use image::math::Rect;
use image::Pixel;
use predicates::PixelToInclude;
use std::ops::IndexMut;

pub mod predicates {
    #[derive(Default)]
    pub struct PixelToInclude {
        pub origin_pixel: [u8; 4],
        pub pixel: [u8; 4],
        pub x_min: u32,
        pub x_max: u32,
        pub y_min: u32,
        pub y_max: u32,
        pub pixel_coordinates: (u32, u32),
    }
    impl PixelToInclude {
        pub fn unlabeled(&self) -> bool {
            self.pixel[3] == 0xff
        }
        pub fn background_within_bounds(&self) -> bool {
            self.x_min <= self.pixel_coordinates.0
                && self.pixel_coordinates.0 <= self.x_max
                && self.y_min <= self.pixel_coordinates.1
                && self.pixel_coordinates.1 <= self.y_max
        }
        pub fn closer_than(&self, distance: u32) -> bool {
            self.pixel[0..3]
                .iter()
                .zip(self.origin_pixel[0..3].iter())
                .map(|(&a, &b)| (b as i32 - a as i32).pow(2u32) as u32)
                .sum::<u32>()
                <= distance.pow(2)
        }
    }
}

pub fn label_image_components_stack<I, P>(
    im: &mut I,
    width: u32,
    height: u32,
    predicate: fn(&PixelToInclude) -> bool,
) -> Vec<Rect>
where
    I: IndexMut<(u32, u32), Output = P>,
    P: Pixel<Subpixel = u8>,
{
    let mut label = 1;
    let mut bounding_boxes: Vec<Rect> = Vec::new();
    let mut stack: Vec<(u32, u32)> = Vec::new();
    let mut pix_buf: [u8; 4] = [0; 4];
    for i in 0..height {
        for j in 0..width {
            let (rgb, alpha) = im[(j, i)].channels_mut().split_at_mut(3);
            if alpha[0] == 0xff {
                // unlabeled
                let (mut x_min, mut x_max, mut y_min, mut y_max) = (j, j, i, i);
                stack.push((j, i));
                im[(j, i)].channels_mut()[3] = 0xff - label;

                while let Some((column, row)) = stack.pop() {
                    x_min = x_min.min(column);
                    x_max = x_max.max(column);
                    y_min = y_min.min(row);
                    y_max = y_max.max(row);
                    pix_buf.clone_from_slice(im[(column, row)].channels());
                    let mut predicate_data = PixelToInclude {
                        x_min,
                        x_max,
                        y_min,
                        y_max,
                        origin_pixel: pix_buf.clone(),
                        ..Default::default()
                    };
                    // 8-connectivity, or inclusion within the bounding box.
                    // This exact algorithm wasn't proven to work. You could instead do separate passes to be sure, buuuuuut, I am tired. And I don't know if that's feasible, either.
                    // Need a better predicate for things like water splashes.
                    for k in row.saturating_sub(1)..(row + 2).min(height) {
                        for l in column.saturating_sub(1)..(column + 2).min(width) {
                            predicate_data.pixel.clone_from_slice(im[(l, k)].channels());
                            predicate_data.pixel_coordinates = (l, k);

                            // unlabeled, or within our bounding rect
                            if predicate(&predicate_data) {
                                let p = im[(l, k)].channels_mut();
                                p[3] = if p[3] == 0xff { 0xff - label } else { 1 };
                                stack.push((l, k));
                            }
                        }
                    }
                }

                bounding_boxes.push(Rect {
                    x: x_min,
                    y: y_min,
                    width: x_max - x_min + 1,
                    height: y_max - y_min + 1,
                });
                // 1 is a sentinel value
                label = (label + 1) % 0xff;
                label += ((label == 0) as u8) << 1;
            }
        }
    }
    bounding_boxes
}

fn label_image_components_stack_generous_bounding_boxes<I, P>(
    im: &mut I,
    width: u32,
    height: u32,
) -> Vec<Rect>
where
    I: IndexMut<(u32, u32), Output = P>,
    P: Pixel<Subpixel = u8>,
{
    let mut label = 1;
    let mut bounding_boxes: Vec<Rect> = Vec::new();
    let mut stack: Vec<(u32, u32)> = Vec::new();
    for i in 0..height {
        for j in 0..width {
            let alpha = im[(j, i)].channels()[3];
            if alpha == 0xff {
                // unlabeled
                let (mut x_min, mut x_max, mut y_min, mut y_max) = (j, j, i, i);
                stack.push((j, i));
                im[(j, i)].channels_mut()[3] = 0xff - label;

                while let Some((column, row)) = stack.pop() {
                    (x_min, x_max, y_min, y_max) = (
                        x_min.min(column),
                        x_max.max(column),
                        y_min.min(row),
                        y_max.max(row),
                    );
                    // 8-connectivity, or inclusion within the bounding box.
                    // This exact algorithm wasn't proven to work. You could instead do separate passes to be sure, buuuuuut, I am tired. And I don't know if that's feasible, either.
                    // Need a better predicate for things like water splashes.
                    for k in row.saturating_sub(1)..(row + 2).min(height) {
                        for l in column.saturating_sub(1)..(column + 2).min(width) {
                            let p = im[(l, k)].channels_mut();
                            // unlabeled, or within our bounding rect
                            if (p[3] != 0 && p[3] != 0xff - label)
                                || (p[3] != 0xff - label
                                    && x_min <= l
                                    && l <= x_max
                                    && y_min <= k
                                    && k <= y_max)
                            {
                                // p[3] = if p[3] == 0xff { 0xff - label } else { 1 };
                                p[3] = 0xff - label;
                                stack.push((l, k));
                            }
                        }
                    }
                    // BUG: No matter what, I cannot get it to work on some pixels that are in fact, inside the final bounding box. Likely has something to do with the fact that they are marked
                    // NOTE: Even after not labeling earlier, this still doesn't change the result.
                    // for l in column.saturating_sub(1)..(column + 2).min(width) {
                    //     for k in row.saturating_sub(1)..(row + 2).min(height) {
                    //         let p = im[(l, k)].channels_mut();
                    //         // unlabeled, or within our bounding rect
                    //         if p[3] == 0xff
                    //             || (p[3] == 0
                    //                 && x_min <= l
                    //                 && l <= x_max
                    //                 && y_min <= k
                    //                 && k <= y_max)
                    //         {
                    //             p[3] = if p[3] == 0xff { 0xff - label } else { 1 };
                    //             stack.push((l, k));
                    //         }
                    //     }
                    // }
                }

                bounding_boxes.push(Rect {
                    x: x_min,
                    y: y_min,
                    width: x_max - x_min + 1,
                    height: y_max - y_min + 1,
                });
                label = (label + 1) % 0xff;
                label += ((label == 0) as u8) << 1;
            }
        }
    }
    bounding_boxes
}
// ASSUMING: Before processing, all alphas are set to 0 or 0xff
fn label_image_components<I, P>(im: &mut I, width: u32, height: u32) -> Vec<Rect>
where
    I: IndexMut<(u32, u32), Output = P>,
    P: Pixel<Subpixel = u8>,
{
    let mut label = 1;
    let mut bounding_boxes: Vec<Rect> = Vec::new();
    for i in 0..height {
        for j in 0..width {
            let alpha = im[(j, i)].channels()[3];
            if alpha == 0xff {
                // unlabeled
                let (x_min, x_max, y_min, y_max) = label_component(im, i, j, width, height, label);

                bounding_boxes.push(Rect {
                    x: x_min,
                    y: y_min,
                    width: x_max - x_min,
                    height: y_max - y_min,
                });
                // MARK: pixels on label change
                // im[(j, i)]
                //     .channels_mut()
                //     .clone_from_slice(&[0xff, 0xff, 0xff, 0xfe]);
                label = (label + 1) % 0xff;
                label += (label == 0) as u8;
            }
        }
    }
    bounding_boxes
}

fn label_component<I, P>(
    im: &mut I,
    row: u32,
    column: u32,
    width: u32,
    height: u32,
    label: u8,
) -> (u32, u32, u32, u32)
where
    I: IndexMut<(u32, u32), Output = P>,
    P: Pixel<Subpixel = u8>,
{
    let (mut x_min, mut x_max, mut y_min, mut y_max) = (column, column, row, row);
    im[(column, row)].channels_mut()[3] = 0xff - label;
    // 8-connectivity
    // Need a better predicate for things like water splashes.
    for i in row.saturating_sub(1)..(row + 2).min(height) {
        for j in column.saturating_sub(1)..(column + 2).min(width) {
            let p = im[(j, i)].channels_mut();
            // unlabeled
            if p[3] == 0xff {
                p[3] = 0xff - label;
                // p[0] = (label % 3) * (0xff >> 1);
                // p[1..3].fill((label % 2) * (0xff));
                let (min_x, max_x, min_y, max_y) = label_component(im, i, j, width, height, label);
                (x_min, x_max, y_min, y_max) = (
                    x_min.min(min_x),
                    x_max.max(max_x),
                    y_min.min(min_y),
                    y_max.max(max_y),
                );
            }
        }
    }

    (x_min, x_max, y_min, y_max)
}
