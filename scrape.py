from playwright.sync_api import sync_playwright
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig
from scipy.special import softmax

import torch
import numpy as np
import time

def error_checking(info) -> bool:
    for i in info:
        if "Browse Other Communities" in i:
            return False
    return True

def scrape_reddit_page_new_posts(page, url) -> str:
        # Navigate to the Reddit page
        page.goto(url)

        time.sleep(5)

        i = 1
        if(i == 1):
            reddit_posts = page.query_selector_all("shreddit-feed shreddit-post")

            text = ""

            i = 0
            for post in reddit_posts:
                if i > 1:
                    post_title = post.query_selector("faceplate-screen-reader-content")
                    title = post_title.inner_text() if post_title else "No title"
                    post_content = post.query_selector("p")
                    content = post_content.inner_text() if post_content else ""
                    if "Previous Actions" in text:
                        text += title + " --(new post)-- "
                    else:
                        text += title + "  " + content + " --(new post)-- "
                i += 1

            return text
        else:
            return "ERROR"

def filter_bitcoin_posts(data, filtered_words):
    filtered_data = [
        post for post in data 
        if any(keyword.lower() in post.lower() for keyword in filtered_words)
    ]
    return filtered_data

def list_to_text(data) -> str:
    text = ""
    for chunk in data:
        text += chunk
    return text

    # Function to process text in chunks
def process_large_text(text, tokenizer, model, config, chunk_size=512) -> list:
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
    text = ""
    result = []
    for i in range(aggregated_scores.shape[0]):
        label = config.id2label[ranking[i]]
        score = aggregated_scores[ranking[i]]
        text = label + " " + str(score)
        result.append(text)
        print(text)
    return result

def main(url, type, text) -> list:
    if type == 'sentiment':
        return sentiment(text)
    else:
        return scrape(url)

def sentiment(text) -> list:
    tokenizer = AutoTokenizer.from_pretrained("mwkby/distilbert-base-uncased-sentiment-reddit-crypto")
    model = AutoModelForSequenceClassification.from_pretrained("mwkby/distilbert-base-uncased-sentiment-reddit-crypto")
    config = AutoConfig.from_pretrained("mwkby/distilbert-base-uncased-sentiment-reddit-crypto")
    return process_large_text(text, tokenizer, model, config)

def scrape(url) -> list:
    with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            page = context.new_page()
            
            # Scrape both Reddit and CoinDesk
            rddt_page_text = scrape_reddit_page_new_posts(page, url)
            browser.close()

    # filtered_data = filter_bitcoin_posts(rddt_page_text)
    text = list_to_text(rddt_page_text)
    tokenizer = AutoTokenizer.from_pretrained("mwkby/distilbert-base-uncased-sentiment-reddit-crypto")
    model = AutoModelForSequenceClassification.from_pretrained("mwkby/distilbert-base-uncased-sentiment-reddit-crypto")
    config = AutoConfig.from_pretrained("mwkby/distilbert-base-uncased-sentiment-reddit-crypto")
    return process_large_text(text, tokenizer, model, config)