# TO VISUALIZE:
- Color distribution (How? Maybe lay them all out)
- Proportion of green
- [X] Why we chose decision trees (visualize test results of SVM, linear and tree regressors, (bar plot with scores))
- Dimensionality reduction
## ML
- [X] Visualize performance of learning based on multiple features
	- [X] Try to change up the kernel for the SVM
	- Do something with those distributions
	- Compute correlation and find a way to visualize it
- [ ] Pickle the model
# Image processing
- Cut out contours
	+ Segmentation algorithms
	+ [X] Detect contours with a filter
	+ Run an algorithm similar to that of detecting parentheses
		- count whites on columns and lines
		- Problem is that we don't know what pixels are opening or closing
		- Could approach from opposite sides, and label everything up to that point as background
- Watershed transform https://docs.opencv.org/4.x/d3/db4/tutorial_py_watershed.html
- [X] Morphological transformations
- Wavelet transform
- [X] HOGs (Histogram of gradient)
	- Okay, but how do we reconcile that different images have different sizes, and that could lead to different number of cells making up the HOG?
		+ Homogenize the number of dimensions.
- Antialiasing
- Downsampling
	+ Mipmap
	+ Box sampling
	+ Sinc
- Clean up images
	+ gamma correction
	+ CLAHE
	+ Noise filters
# Feature selection
- Variance thresholding will do
## Feature dominance
- Majority vote features




# DevOps
- CI/CD
- Unit tests
- deterministic simulation testing blast
- Dockerfile setting up environment
	- Cargo
	- Pip
