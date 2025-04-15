// Title page

= Introduction
The blight is a common plant disease that affects potatoes, making them nigh inedible. Though preventative measures exist, it's difficult to look through an entire field for signs of it. An automated system would help tremendousely in this case. Thankfully, the blight is very easy to spot using potato leaves, meaning it can be detected without even having to unearth the crops.
In this report, we'll be going through 


= Solving the classification problem

== Models
The problem is one about classification, so we decided to try out a few classic classification approaches:
- Decision tree
- SVM with different kernels
- Logistic regression

=== Tree hyperparameter tuning
The decision tree needs a hyperparameter for maximum_depth as to avoid big performance losses for minimal gains in the accuracy of the model.
#figure("visualizations/depth_score.svg")
Here we see the diminishing returns of increasing max_depth for the decision tree. We settled on a max depth of 6.

== Preprocessing
For incoming data we'd like to classify, we follow these steps
+ Crop the image
  - denoise the image using an averaging filter
  - then we apply a morphological transformation to enlarge
  - Apply a convolution with a gradient kernel to detect edges
  - Threshold the resulting image to get something like this
  #figure(image("images/filtered_apple.png"))
  - Find the connected components and their bounding boxes
  - Get the bounding box of those bounding boxes to get the final bounds for the input image
  #figure(image("images/rected_apple.png"))
  - Crop the image
+ Calculate the necessary features
+ Put it all into dataframes to run the model on

