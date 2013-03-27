# -*- coding: utf-8 -*-


#Q = ' '.join(sys.argv[1:])

#MAX_PAGES = 15
#RESULTS_PER_PAGE = 100



def get_search(t,Q,geocode,RESULTS_PER_PAGE,MAX_PAGES):
    search_results = []
    for page in range(1,MAX_PAGES+1):
        if geocode != "":
            search_results += \
                t.search(q=Q,rpp=RESULTS_PER_PAGE, page=page)['results']
        else:
            search_results += \
                t.search(q=Q,geocode=geocode,rpp=RESULTS_PER_PAGE, page=page)['results']
    return search_results