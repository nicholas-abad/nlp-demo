import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from nlp_tasks import question_answering, summarization


external_stylesheets = ["https://codepen.io/roskoN/pen/xxGqxdm.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
flask_app = app.server

# Defining the main Plotly Dash layout.
app.layout = html.Div(
    [
        html.Div(
            className="container",
            children=[
                # Display AT logo.
                html.Img(
                    src=app.get_asset_url("AT_Logo_black-orange-square.png"),
                    style={"width": "15%", "text-align": "center"},
                ),
                html.Br(),
                # Header.
                html.H2(
                    "Choose a task: ",
                    style={"text-align": "center", "font-weight": "bold"},
                ),
                html.Br(),
                # Plotly Dash component for user to upload image.
                dcc.RadioItems(
                    id="task",
                    options=[
                        {'label': 'Question and Answering', 'value': 'Q&A'},
                        {'label': 'Text Summarization', 'value': 'summarization'},
                        {'label': 'Text Generation', 'value': 'generation'}
                    ]
                ),
                html.Br(),
                html.Div(id="task-output"),

                #######################
                ##### HIDDEN DIVS #####
                #######################
                
                # Question and Answering
                dcc.Textarea(id='question-answer-context',style={"visibility": "hidden"}),
                dcc.Textarea(id='question-answer-question',style={"visibility": "hidden"}),
                html.Button('Submit', id='question-answer-submit-button', n_clicks=0, style={"visibility": "hidden"}),
                html.Div(id='question-answer-context-output', style={"visibility": "hidden"}),                

                # Text summarization
                dcc.Textarea(id='summarize-input',style={"visibility": "hidden"}),
                html.Button('Submit', id='summarize-button', n_clicks=0, style={"visibility": "hidden"}),
                html.Div(id='summarize-output', style={"visibility": "hidden"})     


            ],
        )
    ]
)

@app.callback(
    Output("task-output", "children"),
    [Input("task", "value")]
)
def output_task(chosen_task):
    if chosen_task == "Q&A":
        div = html.Div([
                html.H2(
                    "Input Some Context: ",
                    style={"text-align": "center", "font-weight": "bold"},
                ),
                dcc.Textarea(
                    id='question-answer-context',
                    value='Insert some context text here.',
                    style={'width': '100%', 'height': 300},
                ),
                html.H2(
                    "Input A Question: ",
                    style={"text-align": "center", "font-weight": "bold"},
                ),
                dcc.Textarea(
                    id='question-answer-question',
                    value='Ask a question!',
                    style={'width': '100%', 'height': 50},
                ),
                html.Button('Submit', id='question-answer-submit-button', n_clicks=0),
                html.Div(id='question-answer-context-output', style={'whiteSpace': 'pre-line'})
        ])
        return div
    elif chosen_task == "summarization":
        div = html.Div([
                html.H2(
                    "Input The Article That You Want To Summarize: ",
                    style={"text-align": "center", "font-weight": "bold"},
                ),
                dcc.Textarea(
                    id='summarize-input',
                    value='Insert an article here',
                    style={'width': '100%', 'height': 300},
                ),
                html.Button('Submit', id='summarize-button', n_clicks=0),
                html.Div(id='summarize-output', style={'whiteSpace': 'pre-line'})

        ])
        return div
    elif chosen_task == "generation":
        return html.H2("generation", style={"text-align": "center", "font-weight": "bold"})
    else:
        return None

@app.callback(
    Output('question-answer-context-output', 'children'),
    [Input('question-answer-submit-button', 'n_clicks')],
    [State('question-answer-context', 'value'), State('question-answer-question', 'value')]
)
def update_output(n_clicks, context_value, question_value):
    if n_clicks > 0:
        div = []
        answers = question_answering.generate_answers(
            context=context_value,
            questions=[question_value]
        )
        div.append(html.Br()),
        div.append(
            html.H2(
                "Here are you answers: ",
                style={"text-align": "center", "font-weight": "bold"},
                    ),
        )

        # Output each question and answer
        for answer_idx in range(len(answers)):
            div.append(html.Div(f'Question {answer_idx + 1}. {question_value}'))
            div.append(html.Div(f'Answer: {answers[answer_idx]}'))
            div.append(html.Br())
        return html.Div(div)

@app.callback(
    Output('summarize-output', 'children'),
    [Input('summarize-button', 'n_clicks')],
    [State('summarize-input', 'value')]
)
def update_output(n_clicks, summarize_input):
    if n_clicks > 0:
        summary = summarization.summarize_article(summarize_input)
        div = []
        div.append(html.Br())
        div.append(
            html.H2(
                "Here's a Summary: ",
                style={"text-align": "center", "font-weight": "bold"},
                    ),
        )
        div.append(f'{summary}')
        return html.Div(div)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=5050)