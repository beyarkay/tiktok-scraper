---
title: Data Science Project 1
subtitle: Scraping TikTok
author: Boyd Kane (26723077)
toc: false
hyperrefoptions:
- linktoc=all
colorlinks: true
links-as-notes: true
documentclass: IEEEtran
classoption: 12pt
header-includes: |
    \usepackage{pdfpages}
    \usepackage{bm}
    \usepackage{booktabs}
---

\begin{figure}
    \centering
    \includegraphics[width=0.05\textwidth]{img/tiktok.png}
\end{figure}
# Introduction 

TikTok is a popular social media platform, with its success often attributed to
the proprietary algorithm it uses to choose what content to display to which
users. The content entirely consists of short, vertical-format videos (called
TikToks) which are presented to the user sequentially.

The algorithm presents TikToks to a user, and learns what they like based on how
long a user watches a particular TikToks and how they interact with it. Often
certain audio clips can go viral, being used in many different TikToks by many
different creators.

This project does not attempt to analyse the audio or video content of the
TikToks, but rather analyses the numerical quantities associated with the
TikToks. The goal is to explore trends and attempt to find instances where a
particular audio, TikTok, or creator went viral.

It was found that TikTok has an integer overflow error for its top 2 creators
who have over $2^{31}$ likes on their profile (@khaby.lame and @bellapoarch)
which resulted in negative and malformatted likes appearing in their profile
previews.

Many TikToks were found that went viral, accumulating millions of likes in less
than a week. These viral TikToks often preceded the creator gaining hundreds of
thousands of followers.

Often the ratio of likes to comments on a TikToks were similar for a given
creator, implying creators induce a consistent impulse on their viewers to like
or comment, and that this impulse does not change as the TikToks becomes more
popular.

\begin{figure}
    \centering
    \includegraphics[width=0.5\textwidth]{img/khaby.lame.png}
    \caption{\texttt{@khaby.lame}'s profile preview shows negative likes,
    indicative of an integer overflow in the TikTok source code.}
\end{figure}

# Implementation

A scraper for TikTok was written using the python libraries `scrapy`,
`selenium`, and `requests` TODO: links?. It made use of a single spider
`tiktok_spider.py`, and a single `TikTok` item. A pipeline was used to parse
any poorly formatted values into numbers and to ensure the resulting data was
clean.

This crawler was run every hour via a cron job that executed the script
`tiktok_scraper.cron`. The data is saved to `tiktoks.jsonlines`
and then copied via `scp` to the author's machine for analysis.


# Crawl process

This scraper loads the home page of TikTok `https://www.tiktok.com/foryou` and
scrolls through TikToks until data from 100 unique TikToks have been recorded.
These data are then saved to disc for later analysis. Each run of the scraper
takes about 50 minutes, and is initiated at the start of each hour. If the
previous job is still running when the next job starts, the previous job is
killed.

The scraper does not log in to the TikTok website, so the scraper is shown
whatever content the website would show to an anonymous user every time the
scraper starts up. This has the advantage that every scraping run is as similar
as possible, but the disadvantage that the ability of the TikTok algorithm to
tailor TikToks to a user's interests cannot be analysed. This project can be
seen as a broad analysis of the TikTok algorithm.

TikTok has several mechanisms to deter automated scrapers. Selenium is required
as TikTok only presents two TikToks when the home page is initially loaded, and
if JavaScript is disabled then nearly the entire content of the website is
immediately deleted and an error message is shown to the user.

To avoid these, a non-default view of the website is navigated to via Selenium.
This non-default view does not include some of the Captchas, and by using
Selenium for full browser automation, TikToks can be loaded as the crawler
scrapes the website.

# Data scraped

For each time the crawler was shown a TikTok, the following values were
gathered:

- `scraped_at`: The datetime at which the TikTok was scraped.
- `scraped_dt`: The hour at which this scrape run started.
- `upload_dt`: The datetime at which the TikTok was uploaded. Collected
  indirectly by interpreting the first 32 bits of the UUID of a TikToks as a UNIX
  timestamp.
- `hours_diff`: Difference in decimal hours between when we scraped this TikTok
  and the previous time we scraped the same TikTok.
- `url`: The URL of the TikTok.
- `audio`: The name of the audio associated with the TikTok
- `audio_url`: The full URL of the audio associated with the TikTok (the audio
  name given by `audio` need not be unique).
- `likes`: The number of likes on the TikTok.
- `likes_per_hour`: The change in the number of likes divided by `hours_diff`.
  when comparing this TikTok and the previous time we scraped the same TikTok.
- `comments`: The number of comments on this TikTok.
- `comments_per_hour`: The change in the number of `comments` divided by
  `hours_diff`. when comparing this TikTok and the previous time we scraped the
  same TikTok.
- `like_comment_ratio`: The number of likes divided by the number of comments.
- `creator`: The username of the creator of this TikTok. Always starts with an
  `@`.
- `creator_url`: The full URL to the creator's TikTok homepage.
- `creator_followers`: The number of followers that the creator has at the time
  the TikTok was scraped.
- `creator_followers_per_hour`: The change in the number of `creator_followers`
  divided by `hours_diff`. when comparing this TikTok and the previous time we
  scraped the same TikTok.
- `creator_likes`: The total number of likes given to this creator over all
  their TikToks. This value suffers from an integer overflow for values over
  $2^31$, but this overflow has been corrected in pre-processing.
- `creator_likes_per_hour`: The change in the number of `creator_likes` divided
  by `hours_diff`. when comparing this TikTok and the previous time we scraped
  the same TikTok.
- `cumul_count`: The cumulative number of times that this *audio* has been
  scraped by the crawler, across all TikToks scraped so far.
- `cumul_likes`: The cumulative number of likes given to this audio
- `cumul_likes`: The cumulative number of likes given indirectly to this audio
  across all TikToks scraped so far.
- `cumul_comments`: The cumulative number of comments given indirectly to this
  audio across all TikToks scraped so far.

Note that TikTok does not show the fully accurate number of likes and comments.
Instead, a summary like $12.3K$ or $45.6M$ is shown. These instances were
parsed to complete numbers like $12 300$ or $45 600 000$. This has the effect
that the resolution of the values is dependant on the magnitude of those
values; a change of 5000 is visible if that change is from 5000 to 10000, but
it not made visible if the change is from 1000000 to 1 005 000. This will cause
problems in the interpretation of results, as TikToks which increase in the
number of likes or comments at a constant rate will appear to stagnate as the
absolute number of likes or comments increases.

The resulting dataset contains 20 500 observations taken over the 13 day time
period 2022-07-30 to 2022-08-11. There are 1700 unique TikToks, 1400 unique
audio clips, and 1400 unique creators.

# Results

## Defining Viral Content

There is no standardised academic definition for a 'viral' piece of content.
For the purposes of this project, a viral piece of content is one which garners
more interactions per unit time than a significant percent of other content on
the platform. The interactions in question are platform specific but usually
some combination of likes, followers, comments, shares, and saves.

Note that this definition intentionally does not account for how popular
creators with millions of followers will more easily create viral content than
smaller creators orders of magnitude fewer followers. This is because including
the number of followers in the definition of a viral piece of content could
cause a cyclical dependency issue: a viral piece of content could increase the
number of followers the creator has, which could cause the piece of content to
no longer meet the definition of virality.

## Which TikToks saw the greatest increase in likes?
Figure \ref{fig:change_in_likes_top_tiktoks} shows the change in the number of
likes for 10 TikToks over the two weeks that data was gathered, with each
TikTok represented by a different line.

\begin{figure}
    \centering
    \includegraphics[width=0.5\textwidth]{img/change_in_likes_top_tiktoks.pdf}
    \caption{Change in the number of likes for TikToks with the greatest
    increase in the number of likes.}
    \label{fig:change_in_likes_top_tiktoks}
\end{figure}

[This TikTok](https://www.tiktok.com/@surthycooks/video/7128141932953439494) by
[@surthycooks](https://www.tiktok.com/@surthycooks) accumulated five million
likes in as many days, and at it's peak was gaining over 225 likes per hour
(see Figure \ref{fig:most_likes_tiktoks_likes_per_hour})

\begin{figure}
    \centering
    \includegraphics[width=0.5\textwidth]{img/most_likes_tiktoks_likes_per_hour.pdf}
    \caption{Likes per hour for TikToks with the greatest increase in the
    number of likes. The orange rugplot shows every time that TikToks was shown
    to the crawler.}
    \label{fig:most_likes_tiktoks_likes_per_hour}
\end{figure}

One can clearly see the steep slope between 2022-08-06 and 2022-08-08,
indicating that this TikToks was going viral during that time period. 

After 2022-08-09, there is a decrease in the slope as the TikTok continues to
gain views, but not at the rate it previously did.

The TikToks
[2](https://www.tiktok.com/@getgifted_byhannah/video/7127211352669703425) (in
orange) and
[3](https://www.tiktok.com/@tattooislife498/video/7127864843675176194) (in
green) by [@getgifted_byhannah](https://www.tiktok.com/@getgifted_byhannah)
and [@tattooislife498](https://www.tiktok.com/@tattooislife498) respectively
each gained many likes, but not quite at the rate of the TikTok by
@surthycooks. 

Both experienced periods of stagnation, with not many additional likes, and
periods of virality gaining millions of likes in a matter of hours.

The remaining seven TikToks did not appear to have moments of virality as
pronounced as the first three. Rather they slowly accumulated likes over the
period of two weeks..


## Do viral TikToks cause an increase in followers?

Figure \ref{fig:highest_delta_followers_tiktokers_creator_followers} shows the
change in a creator's follower count over time.

\begin{figure}
    \centering
    \includegraphics[width=0.5\textwidth]{img/highest_delta_followers_tiktokers_creator_followers.pdf}
    \caption{The change in the top-6 creator's follower count over time. The
    green rugplot indicates the first time the scraper was shown a new TikTok,
    and the orange rugplot indicates every time the scraper was shown a tiktok
    by that creator.}
    \label{fig:highest_delta_followers_tiktokers_creator_followers}
\end{figure}

Only the creators which experienced the greatest increase in followers are
shown.

It is clear that [@surthycooks](https://www.tiktok.com/@surthycooks)
experienced a massive increase in their follower count after the viral TikToks
was released.

Their followers grew by over 1 million, more than double the growth of the next
creator.

## How to convert likes into followers?

Define the likes-to-followers ratio for a given creator as the number of likes
that creator has divided by the number of followers that same creator has.
Figure \ref{fig:likes_to_followers_ratio_histogram} then shows the frequency of
different likes-to-followers ratios. If the likes-to-followers ratio was over
80, it was excluded due to a few outliers with a likes-to-followers ratio of
over 500. The red lines indicate the $5$-th and $95$-th percentile of the
trimmed data.

This histogram shows that 90% of creators experience one follower for every 4
to 38 likes on a TikToks, with the median of the data being one follower every 12
likes.

This would imply that if a creator can make TikToks which gain many likes, then
some percentage of those likes will result in followers.

\begin{figure}
    \centering
    \includegraphics[width=0.5\textwidth]{img/likes_to_followers_ratio_histogram.pdf}
    \caption{Frequency of various likes-to-followers ratios for all creators.
    Red lines indicate the $5$-th and $95$-th percentile.}
    \label{fig:likes_to_followers_ratio_histogram}
\end{figure}

## Likes to comments ratio

Figure \ref{fig:likes_vs_comments} shows a line plot of the number of likes
vs the number of comments on the top 10 TikToks with the greatest increase in
likes. From this plot we can see that the ratio of likes to comments for a
given TikToks remains approximately constant regardless of how much attention it
gathers.

\begin{figure}
    \centering
    \includegraphics[width=0.5\textwidth]{img/likes_vs_comments.pdf}
    \caption{Likes vs comments on TikToks with the greatest increase in likes.}
    \label{fig:likes_vs_comments}
\end{figure}

This likes to comments ratio can be calculated explicitly and plotted as a
histogram, as shown in Figure \ref{fig:comments_to_likes_ratio_histogram}. This
plot shows that 95% of TikToks will have fewer than 3 comments for every 100 likes
they get.

\begin{figure}
    \centering
    \includegraphics[width=0.5\textwidth]{img/comments_to_likes_ratio_histogram.pdf}
    \caption{Comments to likes ratio, with the red lines indicating the $5$-th
    and $95$-th percentiles.}
    \label{fig:comments_to_likes_ratio_histogram}
\end{figure}

Figure \ref{fig:comments_per_like_against_followers} shows every TikTok made by
every creator.

These TikToks are plotted as a two dimensional heatmap with comments per like
against the log of the number of followers of the creator.

One can see that the most followed creators receive relatively few comments per
like.

This would imply that likes are slightly more closely correlated with followers
than comments are.

It is possible that this is due to the TikTok algorithm favouring likes over
comments, but it could also be that it is easier to like a TikTok or follow
it's creator than it is to leave a comment on a TikTok.

\begin{figure}
    \centering
    \includegraphics[width=0.5\textwidth]{img/comments_per_like_against_followers.pdf}
    \caption{Heatmap of comments per like against followers for every TikTok by
    every creator.}
    \label{fig:comments_per_like_against_followers}
\end{figure}

## Does posting more often correlate with more followers?

Figure \ref{fig:days_since_last_upload_vs_followers} shows the days since a
creator last uploaded a TikTok against their follower count for every TikTok.

From this we can see that there is no particular trend between upload frequency
and follower count. It appears that the majority of creators post within 10
days of their previous TikTok.

\begin{figure}
    \centering
    \includegraphics[width=0.5\textwidth]{img/days_since_last_upload_vs_followers.pdf}
    \caption{Days since last upload against follower count for all creators.}
    \label{fig:days_since_last_upload_vs_followers}
\end{figure}

# A special note

While working on this project, I discovered a bug in seaborn. This bug caused
margins to increase when multiple rugplots were added to the same ax, even if
`expand_margins` is False. To find the root cause was quite complicated, and
but the bug came from how seaborn detects the correct colors to for the
rugplot. In `seaborn/utils.py`, in method `_default_color`, the following line
resolves to `ax.plot([], [], **kws)`:

```py
scout, = method([], [], **kws)
```

By default, matplotlib has the parameters `scalex` and `scaley` of `ax.plot`
set to `True`. Matplotlib would see that the rug was already on the `ax` from
the previous call to `sns.rugplot`, and so it would rescale the x and y axes.
This caused the content of the plot to take up less and less space, with larger
and larger margins as more rugplots were added.

I have fixed this issue (see
[this pull request](https://github.com/mwaskom/seaborn/pull/2953))
and the change will be available in seaborn 0.12, but unfortunately was not
available by the deadline of this project. 

# Figures

\begin{figure}
    \centering
    \includegraphics[width=0.5\textwidth]{img/khaby.lame.png}
    \includegraphics[width=0.5\textwidth]{img/bellapoarch.png}
    \caption{\texttt{@khaby.lame}'s and \texttt{@bellapoarch}'s profile
    previews show negative likes, indicative of an integer overflow}
\end{figure}
