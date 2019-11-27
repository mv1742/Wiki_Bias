# Source of Conflict

## Insight Data Engineering 2019C
## Manrique Vargas (MV), mv1742@nyu.edu
# Data Analysis

<img src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/SoC.png" data-canonical-src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/SoC.png" width="180" height="120" />


1. [Conflict Score](README.md#1.-Conflict-Score)
1. [Relevant Findings](README.md#2.-Relevant-Findings)
1. [Discussion](README.md#3.-Discussion)
1. [Future Work](README.md#4.-Future Work)

# 1. Conflict Score
Source of Conflict is a tool for Wikipedia users and moderators to analyze how some features affect the edit history. I calculate different metrics for and identify which metrics lead to more edits. Conflict is defined by number of reverted articles normalized by total edits and article length. Other features include categories, diversity of references, type of reference, domain, number of edits done by bots. Currently conflictive articles in Wikipedia are manually protected by moderators when necessary. Future work will focus on automating the article protection in Wikipedia using machine learning.

<img src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/Conflict_Score.png" data-canonical-src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/Conflict_Score.png" width="380" height="220" />

# 2. Relevant Findings

This monthly metric is useful to observe activity in conflictive articles. Most reverted articles over the entire Wikipedia history range from popular artists to countries and religious topics. Even though none of the most cited domains do not make it the list, some religous websites are observed among the top 10. The distribution of domains and conflict score was similar for popular domain sources.
Meanwhile the distribution of categories and conflict score showed greater mean variance and upper quartile variance for popular article categories. Therefore it was concluded that conflict is more influenced by categories and topics rather than the reference sources. 

# 3. Discussion

This tool can be used by Wikipedia moderators to monitor contentious articles, potentially automate locking of conflictive articles, and identify recurrently cited sources in conflictive articles. Similarly, public users can understand edit history and conflict and create awareness of articles with higher risk of bias.

# 4. Future Work
Future work could work towards improving causal inference by looking at all the data from meta-history to analyze time-series, The conflict score can also be imporved. For example the Pagerank algorithm to differentiate popular articles. Statistical tests like KS test can be applied to compare distributions and test null hypothesis. In addition, locking conflictive articles can be automated using NLP models.
