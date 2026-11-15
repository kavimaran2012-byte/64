"""
Mini Search Engine web page (Gradio). Step 9 of the activity.
Keep this file in the same folder as search_engine.py and articles.py
Run: python search_engine_app.py then open http://127.0.0.1:7860
Do not use launch(share=True): it makes a public link to your computor.
"""
import gradio as gr
import pandas as pd
import search_engine as se


def run_search(query, ranker):


    if not query.strip():
        return "Type somthing to search.", None
    results = se.search(query, ranker, k=5)
    if not results:
        page = f"### No results for '{query}'\nTry a different word. Why do you think nothing matched?"
    else:
        page = f"_{len(results)} results, ranked bu **{ranker}**_\n\n"
        for title, score in results:
            page += f"### {title}\n...{se.snippet(title, query, bold=True)}... /n score {score:.3f}'\n\n"


            rows = []
            for term in dict.fromkeys(se.tokenize(query)):
                posting = se.INDEX.get(term, {})
                rows.append([term, f"{len(posting)}/{se.N}", round(se.idf(term), 2),
                             ", ".join(se.ARTICLES[d][0] for d in posting) or "-"])
            explain = pd.DataFrame(rows, columns=["word", "in articles","IDF", "found in"])
            return page, explain
        

with gr.Blocks(title="Mini Search Engine") as demo:
    gr.Markdown("# Mini Search Engine\nSwitch rankers and watch the results change.")
    with gr.Row():
        query = gr.Textbox(label="Search", value="thecolours of the rainbow", scale=3)
        ranker = gr.Radio(list(se.RANKERS), value="TF-IDF", label="Ranker", scale=2)
    with gr.Row():
        with gr.Column(scale=3):
            page = gr.Markdown()
        with gr.Column(scale=2):
            gr.Markdown("**Under the hood:** how rare is each word")
            explain = gr.Dataframe()
    gr.Examples([["the history of pizza"], ["lava from a volcano"], ["dinosaur"], ["the"]], inputs=query)

    inputs = [query, ranker]
    outputs = [page, explain]
    for trigger in (query.submit, ranker.change):
        trigger(run_search, inputs, outputs)
    demo.load(run_search, inputs, outputs)

if __name__ == "__main__":
    demo.launch()