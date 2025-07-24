from pyvis.network import Network
import networkx as nx
import os

def generar_red(html_file="/Users/bradrez/Documents/NNProtect_new_website/assets/red.html"):
    # Crear grafo
    G = nx.DiGraph()
    G.add_node("me", label="Yo", size=30, color="orange", title="Usuario principal")
    for u in ["u1","u2","u3"]:
        G.add_node(u, label=u, size=20, color="#00aaff")
        G.add_edge("me", u)
    G.add_node("u1a", label="u1a", size=15, color="#99ddff")
    G.add_edge("u1", "u1a")

    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="#000000")

    net.from_nx(G)
    net.barnes_hut()
    net.show_buttons(filter_=["physics"])

    # Crea el directorio si no existe
    os.makedirs(os.path.dirname(html_file), exist_ok=True)

    # Guarda sin abrir navegador
    net.write_html(html_file)
    print(f"✅ Archivo generado: {html_file}")

if __name__ == "__main__":
    generar_red()