import requests
import openai
from django.core.management.base import BaseCommand
from news.models import Article

# Configuration
GNEWS_API_KEY = 'key'
OPENAI_API_KEY = 'key'
GNEWS_URL = 'https://gnews.io/api/v4/search'
OPENAI_MODEL = 'gpt-4o'  # Update as needed

CATEGORY_KEYWORDS = {
    'national': ['country', 'state', 'local', 'national'],
    'international': ['global', 'international', 'world'],
    'science_technology': ['technology', 'science', 'innovation', 'research'],
    'entertainment': ['celebrity', 'film', 'music', 'tv', 'movie', 'theater', 'cinema', 'trailer', 'incredibles'],
    'business': ['economy', 'business', 'finance', 'market']
}

class Command(BaseCommand):
    help = 'Fetch and process news articles from GNews and store them in the database'

    def handle(self, *args, **options):
        self.stdout.write('Fetching news articles...')
        for category in CATEGORY_KEYWORDS.keys():
            self.stdout.write(f'Fetching news for category: {category}')
            self.fetch_and_store_articles(category)

    def fetch_gnews_articles(self, category):
        keywords = ' OR '.join(CATEGORY_KEYWORDS[category])
        news_query_params = {
            'q': keywords,  # Dynamic query term based on category
            'lang': 'en',
            'country': 'us',
            'max': 10,
            'apikey': GNEWS_API_KEY
        }
        try:
            response = requests.get(GNEWS_URL, params=news_query_params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            self.stdout.write(f"HTTP error occurred: {err}")
            self.stdout.write(f"Response content: {response.text}")
        except Exception as err:
            self.stdout.write(f"An error occurred: {err}")

    def generate_article_summary(self, text):
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Write a detailed, unbiased news article, with verified information based on this reference:\n\n{text}  Please make it readable, and include formatting and paragraph breaks. Do not include a title or a 'by [author]', just body text."}
            ]
        )
        return response.choices[0].message['content'].strip()
            
    def categorize_article(self, body_text):
        for category, keywords in CATEGORY_KEYWORDS.items():
            if any(keyword in body_text.lower() for keyword in keywords):
                return category
        return 'general'  # This should be outside the loop

    
    def is_valid_image_url(self, url):
        try:
            response = requests.head(url)
            content_type = response.headers.get('Content-Type')
            return response.status_code == 200 and content_type.startswith('image')
        except requests.RequestException:
            return False

    def store_article(self, headline, body_text, references, category, image_url=None):
        if not Article.objects.filter(headline=headline).exists():
            Article.objects.create(
                headline=headline,
                body_text=body_text,
                references=references,
                category=category,
                image=image_url
            )
            self.stdout.write(f"Article stored: {headline}")
        else:
            self.stdout.write(f"Article already exists: {headline}")
            
    def fetch_and_store_articles(self, category):
        data = self.fetch_gnews_articles(category)
    
        if data is None:
            self.stdout.write(f"No data received from GNews API for category: {category}")
            return
        
        articles = data.get('articles', [])
        
        for article in articles:
            headline = article.get('title', '')
            body_text = article.get('description', '') or article.get('content', '')
            image_url = article.get('image', '')
            
            if not self.is_valid_image_url(image_url):
                image_url = None
            
            references = article.get('url', '')
            category = self.categorize_article(body_text)
            summary = self.generate_article_summary(body_text) if body_text else body_text
            
            self.store_article(
                headline=headline,
                body_text=summary,
                references=references,
                category=category,
                image_url=image_url
            )

