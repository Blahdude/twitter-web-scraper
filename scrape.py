from playwright.sync_api import sync_playwright
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoConfig
from scipy.special import softmax

import torch
import numpy as np
import time

def scrape_reddit() -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()

        # Navigate to the Reddit page
        page.goto("https://www.reddit.com/r/Bitcoin/")

        time.sleep(5)

        reddit_posts = page.query_selector_all("shreddit-feed shreddit-post")

        final_string = ""

        with open("items.txt", 'w') as file:
            i = 0
            for post in reddit_posts:
                if i > 1:
                    post_name = post.query_selector("faceplate-screen-reader-content")
                    name = post_name.inner_text() if post_name else "No title"
                    post_text = post.query_selector("p")
                    text = post_text.inner_text() if post_text else ""
                    if "Previous Actions" in text:
                        final_string += name + " -- "
                    else:
                        final_string += name + "  " + text + ' -- '
                i += 1

        return final_string

        browser.close()

    # Function to process text in chunks
def process_large_text(text, tokenizer, model, config, chunk_size=512):
    # Tokenize the text
    inputs = tokenizer(text, return_tensors='pt', max_length=chunk_size, truncation=True)
    input_ids = inputs['input_ids'][0]

    # If the text is too long, split it into chunks
    if len(input_ids) > chunk_size:
        num_chunks = len(input_ids) # chunk_size + (1 if len(input_ids) % chunk_size > 0 else 0)
        chunks = [input_ids[i*chunk_size:(i+1)*chunk_size] for i in range(num_chunks)]
    else:
        chunks = [input_ids]

    # Process each chunk
    scores_list = []
    for chunk in chunks:
        chunk_input = {'input_ids': chunk.unsqueeze(0)}
        with torch.no_grad():
            output = model(**chunk_input)
            logits = output.logits.detach().numpy()
            scores = softmax(logits[0])
            scores_list.append(scores)

    # Aggregate results (e.g., average the scores)
    aggregated_scores = np.mean(scores_list, axis=0)
    ranking = np.argsort(aggregated_scores)
    ranking = ranking[::-1]

    # Print rankings
    for i in range(aggregated_scores.shape[0]):
        label = config.id2label[ranking[i]]
        score = aggregated_scores[ranking[i]]
        print(f"{i+1}) {label} {np.round(float(score), 4)}")

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
config = AutoConfig.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")

text = scrape_reddit()
# Process the large text
process_large_text(text, tokenizer, model, config)