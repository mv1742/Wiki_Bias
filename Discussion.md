# Source of Conflict

## Insight Data Engineering 2019C
## Manrique Vargas (MV), mv1742@nyu.edu
# Data Analysis

<img src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/SoC.png" data-canonical-src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/SoC.png" width="180" height="120" />


1. [Discussion](README.md#3.-Discussion) 

## 1.1 Relevant Findings

The monthly metric of conflict is useful to observe monthly activity in the edit history of articles. Most reverted articles over the entire Wikipedia history range from popular artists to countries and religious topics. Even though none of the most cited domains do not make it the list, some religous websites are observed among the top 10. The distribution of domains and conflict score was similar for popular domain sources.
Meanwhile the distribution of categories and conflict score showed greater mean variance and upper quartile variance for popular article categories. Therefore it was concluded that conflict is more influenced by categories and topics rather than the reference sources.

<img src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/Monthly_Metrics.png" data-canonical-src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/Monthly_Metrics.png" width="680" height="220" /> 
__Figure 1.__ The bar chart above shows monthly reverts for August 2019, one of Source of Conflict Dashboard metrics. Users can select any month they want from Wikipedia data.

## 1.2 Applications

This tool can the following applications:
- Wikipedia moderators: 
    - Monitor contentious articles
    - Potentially automate locking of conflictive articles
    - I dentify recurrently cited sources in conflictive articles 
 - Public users 
    - Understand edit history and conflict
    - Create awareness of articles with higher risk of bias

## 1.3 Future Work

 - Future work can work towards improving causal inference by looking at all the data from meta-history to analyze time-series. 
 - The conflict score can also be improved. For example the Pagerank algorithm to differentiate popular articles.

Conflict is defined by number of reverted articles normalized by total edits and article length. The conflict scores are first standarized and then added. The resulting distribution is then divided into 5 levels of conflict, 1 indicating less conflictive and 5 more conflictive.
Normalization is done to compare articles and remove factors like popularity, length. Future Work should improve this normalization.

<img src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/Conflict_Score.png" data-canonical-src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/Conflict_Score.png" width="680" height="220" />
__Figure 2.__ Conflict Score Distribution
 
 - Statistical tests like KS test can be applied to compare distributions and test null hypothesis. 
 - In addition, locking contentious articles can be automated using NLP models.

