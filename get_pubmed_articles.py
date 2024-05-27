from Bio import Entrez
import pandas as pd

#Enter your email id
Entrez.email = ""

def search(query, max_articles):
  """
  Retrieves the 'max_articles' based on the provided query
  """
  handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax=max_articles,
                            retmode='xml',
                            term=query)
  results = Entrez.read(handle)
  return results

def fetch_details(id_list):
  """
  Fetch the metadata of PubMed articles based on their IDs
  """
  ids = ','.join(id_list)
  handle = Entrez.efetch(db='pubmed',
                        retmode='xml',
                        id=ids)
  results = Entrez.read(handle)
  return results

def get_pubmed_data(search_term="diabetes",start_date="2023/01/01",end_date = "2024/01/01",max_articles=10000):
  """
  Retrieves the first max_articles from pubmed and returns in a pandas dataframe.
  """

  date_range = start_date + ":" + end_date
  query = f"{search_term}[All Fields] AND ({date_range}[Date - Publication])"
  #Get the ids of the retrieved articles
  results = search(query, max_articles = max_articles)
  id_list = results['IdList']
  # Fetch details of retrieved articles
  papers = fetch_details(id_list)

  result = []
  for i, paper in enumerate(papers['PubmedArticle']):
    abstract = paper['MedlineCitation']['Article'].get('Abstract')
    date = paper['MedlineCitation']['Article']['ArticleDate']
    if abstract and date:
      r = {
                "title": paper['MedlineCitation']['Article']['ArticleTitle'],
                "abstract": abstract['AbstractText'][0],
                "pub_date": paper['MedlineCitation']['Article']['ArticleDate'][0]['Year'] + "-" + paper['MedlineCitation']['Article']['ArticleDate'][0]['Month'] + \
                             "-" +  paper['MedlineCitation']['Article']['ArticleDate'][0]['Day'],
                "journal": paper['MedlineCitation']['Article']['Journal']['Title']
            }
      result.append(r)
    else:
      pass

  df_pubmed = pd.DataFrame.from_dict(result)
  return df_pubmed

if __name__ == "__main__":
  search_term = "diabetes"
  start_date = "2022/01/01"
  end_date = "2024/01/01"
  df_pubmed = get_pubmed_data(search_term="diabetes",start_date="2023/01/01",end_date = "2024/01/01",max_articles=10000)
  df_pubmed.to_parquet("Pubmed_abstract_10k.parquet")