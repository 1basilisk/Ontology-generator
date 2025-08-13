#!/usr/bin/env python3
"""
visualize.py
Pyvis-based ontology visualizer (rdflib -> interactive HTML).

Usage:
    python visualize.py path/to/ontology.ttl [output.html]
"""

import sys
import os
import html
from rdflib import Graph, RDF, RDFS, OWL, URIRef, Literal
from pyvis.network import Network

def qname_or_str(g: Graph, uri):
    """Try to return a compact qname prefix:LocalName, otherwise the local name, else full URI."""
    try:
        return g.namespace_manager.qname(uri)
    except Exception:
        try:
            # fallback to splitting by '#' or '/'
            s = str(uri)
            if '#' in s:
                return s.split('#')[-1]
            if '/' in s:
                return s.rsplit('/', 1)[-1]
            return s
        except Exception:
            return str(uri)

def safe_html_label(text: str) -> str:
    """Escape text for HTML then return. Wrap tags (b/i) added by caller."""
    return html.escape(text)

def visualize_ontology(ttl_file, output_html="output/ontology_visualization.html", height="900px", width="100%"):
    if not os.path.exists(ttl_file):
        raise FileNotFoundError(f"TTL file not found: {ttl_file}")

    # Load graph
    g = Graph()
    g.parse(ttl_file, format="turtle")

    # Create Pyvis network
    net = Network(height=height, width=width, directed=True, bgcolor="#ffffff")
    # reduced repulsion / shorter springs => nodes closer together
    net.set_options("""
{
  "nodes": {
    "font": { "multi": "html", "size": 18 },
    "shapeProperties": { "borderRadius": 12 }
  },
  "edges": {
    "font": { "multi": "html", "size": 14 },
    "arrows": { "to": { "enabled": true, "type": "arrow" } },
    "smooth": { "enabled": true, "type": "dynamic" }
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -8000,
      "springLength": 100,
      "springConstant": 0.001
    },
    "minVelocity": 0.5
  }
}
""")

    added_nodes = set()

    def add_node_if_missing(node_id: str, label_html: str, color="#8ecae6", shape="box", size=60):
        """Add a node once. size is visual diameter in px; font scaled."""
        if node_id in added_nodes:
            return
        # Set font size proportional to node size for legibility
        font_size = max(12, int(size * 0.25))
        net.add_node(node_id, label=label_html, color=color, shape=shape, size=size,
                     font={"multi": "html", "size": font_size})
        added_nodes.add(node_id)

    # 1) Add declared classes (RDFS.Class and OWL.Class)
    class_nodes = set()
    for c in g.subjects(RDF.type, RDFS.Class):
        if isinstance(c, URIRef):
            class_nodes.add(c)
    for c in g.subjects(RDF.type, OWL.Class):
        if isinstance(c, URIRef):
            class_nodes.add(c)

    for c in class_nodes:
        qn = qname_or_str(g, c)
        label = f"<b>{safe_html_label(qn)}</b>"
        add_node_if_missing(str(c), label, color="#8ecae6", shape="box", size=80)

    # 2) Add other URI subjects we may encounter (as boxes)
    for s in set(g.subjects()):
        if isinstance(s, URIRef):
            sid = str(s)
            if sid not in added_nodes:
                qn = qname_or_str(g, s)
                label = f"<b>{safe_html_label(qn)}</b>"
                add_node_if_missing(sid, label, color="#8ecae6", shape="box", size=60)

    # 3) Walk triples and add edges/nodes for objects and literals
    for s, p, o in g.triples((None, None, None)):
        # Skip class declarations we've already painted as boxes
        if p == RDF.type and (o == RDFS.Class or o == OWL.Class):
            continue

        # short predicate label
        p_label_short = qname_or_str(g, p) if isinstance(p, URIRef) else str(p)
        p_label_html = f"<i>{safe_html_label(p_label_short)}</i>"

        subj_id = str(s)
        if subj_id not in added_nodes:
            subj_qn = qname_or_str(g, s) if isinstance(s, URIRef) else str(s)
            subj_label = f"<b>{safe_html_label(subj_qn)}</b>" if isinstance(s, URIRef) else safe_html_label(str(s))
            add_node_if_missing(subj_id, subj_label, color="#8ecae6", shape="box", size=60)

        if isinstance(o, Literal):
            # deterministic literal node id to avoid duplicates across same literal
            lit_hash = abs(hash((str(o), p_label_short, subj_id)))
            lit_id = f"lit:{lit_hash}"
            lit_label = safe_html_label(str(o))
            if lit_id not in added_nodes:
                add_node_if_missing(lit_id, f"{lit_label}", color="#fefae0", shape="ellipse", size=30)
            net.add_edge(subj_id, lit_id, label=p_label_html, color="#ffb703")
        elif isinstance(o, URIRef):
            obj_id = str(o)
            if obj_id not in added_nodes:
                qn = qname_or_str(g, o)
                add_node_if_missing(obj_id, f"<b>{safe_html_label(qn)}</b>", color="#8ecae6", shape="box", size=60)

            # Determine if predicate is object or datatype property
            is_object_prop = True
            if (p, RDF.type, OWL.DatatypeProperty) in g:
                is_object_prop = False
            elif (p, RDF.type, OWL.ObjectProperty) in g:
                is_object_prop = True
            else:
                # heuristic: object is URIRef -> object property
                is_object_prop = True

            # Edge color by property type
            edge_color = "#219ebc" if is_object_prop else "#ffb703"
            net.add_edge(subj_id, obj_id, label=p_label_html, color=edge_color)
        else:
            # fallback node for blank nodes or other types
            unk_id = f"node:{abs(hash((str(o), p_label_short, subj_id)))}"
            if unk_id not in added_nodes:
                add_node_if_missing(unk_id, safe_html_label(str(o)), color="#e0e0e0", shape="ellipse", size=36)
            net.add_edge(subj_id, unk_id, label=p_label_html, color="#999999")

    # 4) Final adjustments: optionally enlarge individuals or tweak visuals
    # Save interactive HTML
    net.write_html(output_html)
    print(f"Ontology visualization saved to {output_html}")

if __name__ == "__main__":
    o = "output/final_ontology.ttl"
    f = "data/ontology_fragments/5.pdfpage_1.txt_0.ttl"
    visualize_ontology(o)