# Source of Conflict

## Insight Data Engineering 2019C
## Manrique Vargas (MV), mv1742@nyu.edu
# Data Analysis

<img src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/SoC.png" data-canonical-src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/SoC.png" width="180" height="120" />


1. [Conflict Score](README.md#1.-Conflict-Score)
1. [Relevant Findings](README.md#2.-Relevant-Findings)
1. [Discussion](README.md#3.-Discussion)
1. [Future Work](README.md#4.-Future-Work)

# 1. Conflict Score
Conflict is defined by number of reverted articles normalized by total edits and article length. The conflict scores are first standarized and then added. The resulting distribution is then divided into 5 levels of conflict, 1 indicating less conflictive and 5 more conflictive.

<img src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/Conflict_Score.png" data-canonical-src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/Conflict_Score.png" width="680" height="220" />

# 2. Relevant Findings

The monthly metric of conflict is useful to observe activity in conflictive articles. Most reverted articles over the entire Wikipedia history range from popular artists to countries and religious topics. Even though none of the most cited domains do not make it the list, some religous websites are observed among the top 10. The distribution of domains and conflict score was similar for popular domain sources.
Meanwhile the distribution of categories and conflict score showed greater mean variance and upper quartile variance for popular article categories. Therefore it was concluded that conflict is more influenced by categories and topics rather than the reference sources. 

# 3. Discussion

This tool can be used by Wikipedia moderators to monitor contentious articles, potentially automate locking of conflictive articles, and identify recurrently cited sources in conflictive articles. Similarly, public users can understand edit history and conflict and create awareness of articles with higher risk of bias.

# 4. Future Work
 - Future work can work towards improving causal inference by looking at all the data from meta-history to analyze time-series. 
 - The conflict score can also be improved. For example the Pagerank algorithm to differentiate popular articles. 
 - Statistical tests like KS test can be applied to compare distributions and test null hypothesis. 
 - In addition, locking conflictive articles can be automated using NLP models.
