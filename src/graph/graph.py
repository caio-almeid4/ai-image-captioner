from langgraph.graph import END, START, StateGraph

from src.graph.nodes.image_analyzer import analyze_image
from src.models.graph import State

graph = StateGraph(State)

graph.add_node('image_analyzer', analyze_image)

graph.add_edge(START, 'image_analyzer')
graph.add_edge('image_analyzer', END)

graph_app = graph.compile()
