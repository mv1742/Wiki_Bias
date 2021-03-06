html_layout = '''<!DOCTYPE html>
                    <html>
                        <head>
                            {%metas%}
                            <title>{%title%}</title>
                            {%favicon%}
                            {%css%}
                        </head>
                        <body>
                            <nav>
  <a href="/"><i class="fas fa-home"></i> Home</a>
              <a href="/month/"><i class="fas fa-chart-line"></i> Month </a>
        <a href="/timeseries/"><i class="fas fa-chart-line"></i> Time Series </a>
           <a href="/articles/"><i class="fas fa-chart-line"></i> Articles </a>
    <a href="/analytics/"><i class="fas fa-chart-line"></i> Domains</a>
       <a href="/categories/"><i class="fas fa-chart-line"></i>Categories</a>
    <a href="/word_cloud/"><i class="fas fa-chart-line"></i>Word Cloud</a>
   <a href="/search/"><i class="fas fa-book"></i> Search</a>
   <a href="/dashapp/"><i class="fas fa-balance-scale"></i>Tables</a>
                            </nav>
                            {%app_entry%}
                            <footer>
                                {%config%}
                                {%scripts%}
                                {%renderer%}
                            </footer>
                        </body>
                    </html>'''
