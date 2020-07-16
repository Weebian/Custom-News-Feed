
from newsapi.newsapi_client import NewsApiClient #Modules for news
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, make_response, jsonify #flask for web stuff
app = Flask(__name__)

#cd E:\Code\Python\Custom News Feed
#env\Scripts\activate
#flask run
#http://127.0.0.1:5000/

#set FLASK_APP=main.py

#variables
newsapi = NewsApiClient(api_key='xxxxx')
current_date = datetime.today().date()
three_days = (current_date - timedelta(days=3)).isoformat()

#routes
@app.route('/')
def home():
    #Retrieve data
    tech = retrieve_top_news_df('technology', True, False, 'https://wallpapercave.com/wp/wp5134538.jpg')
    cyber_security = retrieve_top_news_df('cyber security', False, False, 'https://www.nzfilm.co.nz/sites/default/files/styles/ratio_16_x_9__small_/public/2017-10/locations_gallery/media/159005/060_sm_3010_1085-640x346.jpg?itok=3hfj5soE')
    canada = retrieve_top_news_df('canada', True, True, 'https://images.dailyhive.com/20170921130857/anime-main-cover.png')
    ottawa = retrieve_top_news_df('ottawa', False, False, 'https://i.pinimg.com/originals/48/b3/95/48b395c55ecc2b8bc4fc0812dec3a30e.jpg')
    anime = retrieve_top_news_df('anime', False, False, 'https://labourenergy.org/wp-content/uploads/2019/11/cute-anime-pictures.jpg')
    manga = retrieve_top_news_df('manga', False, False, 'https://wallpapercave.com/wp/wp6856720.jpg')

    return render_template(
        'home.html',
        categories = [tech, cyber_security, canada, ottawa, anime, manga],
    )

@app.route('/article')
def article_page():
    return render_template(
        'article.html',
        source = request.args.get("source"),
        author = request.args.get("author"),
        content = request.args.get("content"),
        description = request.args.get("description"),
        publishedAt = request.args.get("publishedAt"),
        title = request.args.get("title"),
        url = request.args.get("url"),
        urlToImage = request.args.get("urlToImage"),
    )

#Function to retrieve the top news in a category
#
#@param keyword the specific keyword for news
#@param is_category identifies if the keyword is q or category
def retrieve_top_news_df(keyword, is_category, is_country, default_image_url):
    #Determine which method to use to obtain the news
    if is_category:
        if is_country:
            data = newsapi.get_top_headlines(country='ca', language='en', page_size = 100)
        else:
            data = newsapi.get_top_headlines(country='ca', category=keyword, language='en', page_size = 100)

    else:
        data = newsapi.get_everything(q=keyword, language='en', from_param=three_days, page_size = 100)

    #store info into dictionnary
    return {
        "name": keyword.capitalize(),
        "status": data['status'].upper(),
        "default_image_url": default_image_url,
        "articles": data['articles']
    }


'''
#retrieve data

tech_data = newsapi.get_top_headlines(category='technology', language='en', page_size = 100)
#canada_data = newsapi.get_top_headlines(country=ca, language='en', page_size = 100)
#anime_data = newsapi.get_everything(q='anime', language='en', from_param=three_days, page_size = 100)
#manga_data = newsapi.get_everything(q='manga', language='en', from_param=three_days, page_size = 100)
#manga_data = newsapi.get_everything(q='light novel', language='en', from_param=three_days, page_size = 100)

#Obtain info
tech_status = tech_data['status']
tech_articles = tech_data['articles']


ca_status = canada_data['status']
ca_articles = canada_data['articles']
num_ca = canada_data['totalResults']

anime_status = anime_data['status']
anime_articles = anime_data['articles']
num_anime = anime_data['totalResults']

manga_status = manga_data['status']
manga_articles = manga_data['articles']
num_manga = manga_data['totalResults']

tech_df = pd.DataFrame(tech_articles)
#anime_df = pd.DataFrame(anime_articles)
#manga_df = pd.DataFrame(manga_articles)
print(tech_df)
#print(anime_df)
#print(manga_df)
'''
if __name__ == '__main__':
    app.run(debug=True)