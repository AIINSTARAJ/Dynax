from crossref.restful import Works

def search_publications(query, max_results=72, sort_by='relevance'):
    """
    Search for publications in Crossref by query
    
    Parameters:
    query (str): The search query
    max_results (int): Maximum number of results to return
    sort_by (str): Sort by 'relevance', 'citations', or 'year'
    
    Returns:
    list: List of publication dictionaries
    """
    works = Works()

    search_results = works.query(query).order('asc')
    
    # Convert iterator to list, but limit to max_results
    results = []
    count = 0
    for item in search_results:
        results.append(item)
        count += 1
        if count >= max_results:
            break
    
    if sort_by == 'citations':
        results = sorted(results, key=lambda x: x.get('is-referenced-by-count', 0), reverse=True)
    elif sort_by == 'year':
        results = sorted(results, key=lambda x: x.get('published', {}).get('date-parts', [[0]])[0][0], reverse=True)
    
    publications = []
    for result in results:
        
        authors = []
        for author in result.get('author', []):
            if 'given' in author and 'family' in author:
                authors.append(f"{author['given']} {author['family']}")
            elif 'family' in author:
                authors.append(author['family'])
                
        pub_info = {
            'title': result.get('title',"Not Available"),
            'authors': ', '.join(authors),
            'year': result.get('published', {}).get('date-parts', [[0]])[0][0] if result.get('published') else 'Not available',
            'citations': result.get('is-referenced-by-count', 'Not available'),
            'url': result.get('URL', 'Not available'),
            'abstract': result.get('abstract', 'Not available'),
            'doi': result.get('DOI', 'Not available'),
            'publisher': result.get('publisher', 'Not available'),
            'publication': result.get('container-title', ['Not available'])[0] if result.get('container-title') else 'Not available',
            'journal_type': result.get('type', 'Not available'),
        }
        publications.append(pub_info)
    
    return publications


def get_publication_by_doi(doi):
    """
    Get publication details by DOI
    
    Parameters:
    doi (str): The DOI of the publication
    
    Returns:
    dict: Publication information or None if not found
    """
    works = Works()
    try:
        item = works.doi(doi)
        
        if item:
            
            authors = []
            for author in item.get('author', []):
                if 'given' in author and 'family' in author:
                    authors.append(f"{author['given']} {author['family']}")
                elif 'family' in author:
                    authors.append(author['family'])
                    
            pub_info = {
                'title': item.get('title', ['No title available'])[0] if item.get('title') else 'No title available',
                'authors': ', '.join(authors),
                'year': item.get('published', {}).get('date-parts', [[None]])[0][0] if item.get('published') else 'Not available',
                'citations': item.get('is-referenced-by-count', 0),
                'doi': item.get('DOI', 'Not available'),
                'url': item.get('URL', 'Not available'),
                'abstract': item.get('abstract', 'Not available'),
                'publisher': item.get('publisher', 'Not available'),
                'publication': item.get('container-title', ['Not available'])[0] if item.get('container-title') else 'Not available',
                'journal_type': item.get('type', 'Not available')
            }
            
            return pub_info
        else:
            return None
    except Exception as e:
        print(f"Error retrieving DOI {doi}: {str(e)}")
        return None
    