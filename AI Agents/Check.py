from model import load_model
llm = load_model()
print(type(llm))
print(hasattr(llm, "bind_tools"))