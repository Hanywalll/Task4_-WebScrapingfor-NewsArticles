import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin, urlparse

class DetikScraper:
    def __init__(self):
        self.base_url = "https://www.detik.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_search_results(self, query, max_pages=3):
        all_articles = []
        for page_num in range(1, max_pages + 1):
            search_url = f"{self.base_url}/search/searchall?query={query}&sortby=time&page={page_num}"
            
            try:
                response = requests.get(search_url, headers=self.headers, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                article_containers = soup.find_all(['article', 'div'], class_=re.compile(r'(article|list|news|item)'))
                
                if not article_containers:
                    article_containers = soup.select('[data-article-url], .list-article, .news-item')
                    
                if not article_containers:
                    break

                for container in article_containers:
                    link_elem = container.find('a', href=True)
                    if not link_elem:
                        continue
                    
                    link = link_elem['href']
                    if not link.startswith('http'):
                        link = urljoin(self.base_url, link)
                    
                    parsed_url = urlparse(link)
                    if 'detik.com' not in parsed_url.netloc:
                        continue
                    
                    if any(x in link for x in ['/tag/', '/video/', '/foto-news/', '/20detik/', '20.detik.com', '/foto-', '/in-depth']):
                        continue
                    
                    title_elem = (container.find(['h2', 'h3', 'h4'], class_=re.compile(r'(title|headline)')) or 
                                  container.find('a', class_=re.compile(r'(title|headline)')) or 
                                  link_elem)
                    
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text().strip()
                    if not title or len(title) < 10:  
                        continue
                    
                    article_data = self.scrape_article_details(link)
                    if article_data:
                        article_data['title'] = title
                        article_data['url'] = link
                        all_articles.append(article_data)
                
                time.sleep(1) 

            except requests.exceptions.RequestException as e:
                break
            except Exception as e:
                continue

        return all_articles

    def scrape_article_details(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            is_detik_pop = 'pop.' in url or 'detikpop' in url
            
            body_text = "Teks artikel tidak ditemukan"
            
            if is_detik_pop:
                body_selectors = [
                    'div.detail__body-text',
                    'div.detail-content',
                    'article.detail__body',
                    'div.artikel'
                ]
            else:
                body_selectors = [
                    'div.detail__body-text',
                    'div.detail_content',
                    'div.jw-detail-text',
                    'div.artikel-body'
                ]
            
            for selector in body_selectors:
                body_container = soup.select_one(selector)
                if body_container:
                    paragraphs = body_container.find_all('p')
                    extracted_text = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                    if extracted_text and len(extracted_text) > 50: 
                        body_text = extracted_text
                        break
            
            image_link = "N/A"
            image_selectors = [
                'div.detail__media-image img',
                'div.pic_art img',
                'div.article_thumb img',
                'figure.article__media img',
                'div.artikel-image img', 
                'figure.photo-detail img',
                'img.preview-image'
            ]
            
            for selector in image_selectors:
                img_elem = soup.select_one(selector)
                if img_elem:
                    src = (img_elem.get('src') or 
                           img_elem.get('data-src') or 
                           img_elem.get('data-original'))
                    
                    if src:
                        if '?' in src:
                            src = src.split('?')[0]
                        
                        if not src.startswith('http'):
                            src = urljoin(self.base_url, src)
                        
                        image_link = src
                        break
            
            pub_time = "N/A"
            time_selectors = [
                'div.detail__date',
                'div.article-date',
                'time.date',
                '[datetime]',
                'div.date'
            ]
            
            for selector in time_selectors:
                time_elem = soup.select_one(selector)
                if time_elem:
                    if time_elem.get('datetime'):
                        pub_time = time_elem['datetime']
                    else:
                        pub_time_text = time_elem.get_text().strip()
                        
                        time_patterns = [
                            r'(\d{2}:\d{2} WIB)',
                            r'(\d{2}:\d{2})',
                            r'(\d{1,2} [A-Za-z]+ \d{4}, \d{2}:\d{2})'
                        ]
                        
                        for pattern in time_patterns:
                            match = re.search(pattern, pub_time_text)
                            if match:
                                pub_time = match.group(1)
                                break
                        
                        if pub_time == "N/A":
                            pub_time = pub_time_text
                    
                    break

            return {
                "image_link": image_link,
                "body_text": body_text,
                "publication_time": pub_time
            }

        except Exception as e:
            return None
