= Feature visualizations
== Visualization code
+ Histogram code
#block(
  fill: luma(230),
  inset: 8pt,
  radius: 4pt,
  raw(read("assets/histograms.py"), lang: "python")
)

+ Boxplot code
#block(
  fill: luma(230),
  inset: 8pt,
  radius: 4pt,
  raw(read("assets/boxplots.py"), lang: "python")
)



== Green distribution
// INTERPRETATION
#figure(image("visualizations/g_channel_dist.svg", width: 70%))
#figure(image("visualizations/G_channel_hist.png", width: 70%))
== Red distribution
// INTERPRETATION
#figure(image("visualizations/r_channel_dist.svg", width: 70%))
#figure(image("visualizations/R_channel_hist.png", width: 70%))
== Blue distribution
// INTERPRETATION
#figure(image("visualizations/b_channel_dist.svg", width: 70%))
#figure(image("visualizations/B_channel_hist.png", width: 70%))

The healthy distribution mode seems to always lie in the middle for the mean. A possible indication that a sign of early blight, is the brightening (the slight yellow tinge) of the leaves. Then, in the late stages, the dark spots bring down the mean rgb values overall.
Note that the red mean component seems to be the most distinct among the three categories.

== Convexity ratio
#figure(image("visualizations/cr_dist.svg", width: 70%))
The convexity ratio shows that the blight doesn't do too much to deform the leaves.
Instead, We see more outliers and a greater variance withe more deteriorating health.
That is, the blight *may* deform a leaf, but it's not for certain.

= Model comparisons
// INTERPRETATION
@depth_score shows the number of tests passed for each depth value. We notice that after a certain threshold, the number of tests doesn't go up any further

#figure(
  image("visualizations/depth_score.svg", width: 80%),
  caption: [Tests passed for each value of max_depth],
) <depth_score>
