use image::math::Rect;
use image::{ImageReader, Pixel};
use segrs::*;
use std::fs::OpenOptions;
use std::io::{BufReader, BufWriter};

fn main() {
    let mut args = std::env::args().skip(1);

    // TODO: If we're cropping, then we'll need a croppee input AND output.
    // Just treat the third argument as the output

    let image_arg = args.next();
    let fst_arg = args.next();
    let snd_arg = args.next();

    let Some(output_path) = fst_arg else {
        panic!("Expected a second argument <image_path> <output_path> [<croppee_path>]");
    };

    let image_path = image_arg.expect("input path missing");

    // split spritesheet
    // ASSUMPTION: Every connected component has a square of empty space surrounding them
    // GOAL: Find connected components
    let f = BufReader::new(
        OpenOptions::new()
            .read(true)
            .write(false)
            .open(image_path.as_str())
            .unwrap(),
    );

    let ext = image_path
        .rfind('.')
        .map(|i| image_path[i + 1..].to_lowercase());
    let im = match ext.as_ref().map(|x| x.as_str()) {
        Some("jpeg") => ImageReader::with_format(f, image::ImageFormat::Jpeg)
            .decode()
            .unwrap(),
        Some("png") => ImageReader::with_format(f, image::ImageFormat::Png)
            .decode()
            .unwrap(),
        _ => ImageReader::new(f).decode().unwrap(),
    };
    // Image graph needs to have non transparent pixels as nodes, and each two adjacent pixels have edges between them
    // Traverse then label pixels as you see them.
    // LABELING SCHEME : We have pixels that are either completely transparent (0,0,0,0), or otherwise. So to say that the pixel is labeled, just set its alpha to its label (starting from 1)

    let mut image_graph: image::ImageBuffer<image::Rgba<u8>, Vec<u8>> = im
        // .sub_image(0, 0, 64 * 4, 64 * 4)
        // .to_image()
        .to_rgba8();
    let (w, h) = (image_graph.width(), image_graph.height());
    let mut bounding_rects: Vec<(Rect, (u32, u32))> =
        label_image_components_stack(&mut image_graph, w, h, |p| {
            p.unlabeled() && (p.closer_than(100))
        })
        .into_iter()
        .map(|rect| (rect, (rect.x + rect.width >> 1, rect.y + rect.height >> 1)))
        .collect();
    assert_eq!(
        image_graph
            .pixels()
            .enumerate()
            .find(|(_, p)| p.channels()[3] == 0xff),
        None
    );
    for p in image_graph.pixels_mut() {
        let alpha = &mut p.channels_mut()[3];
        if *alpha < 2 {
            *alpha = 0;
        } else {
            *alpha = 0xff;
        }
    }
    // drawing bounding rects
    for (
        Rect {
            x,
            y,
            width,
            height,
        },
        _,
    ) in bounding_rects.iter().cloned()
    {
        for i in y..y + height {
            // purple border
            let col = image::Rgba::from([0xff, 0, 0xff, 0xff]);
            image_graph.put_pixel(x, i, col);
            image_graph.put_pixel(x + width - 1, i, col);
        }
        for j in x..x + width {
            // green bottom
            let col = image::Rgba::from([0, 0xff, 0, 0xff]);
            image_graph.put_pixel(j, y, col);
            image_graph.put_pixel(j, y + height - 1, col);
        }
    }

    // TODO: When computing the bigger bounding box, don't use every single bounding box.
    // Draw the contour bounding box
    let main_bound = {
        let [x_min, y_min, x_max, y_max] = bounding_rects.iter().skip(1).filter(|_| true).fold(
            [u32::MAX, u32::MAX, u32::MIN, u32::MIN],
            |[x_min, y_min, x_max, y_max],
             (
                Rect {
                    x,
                    y,
                    width,
                    height,
                },
                _,
            )| {
                [
                    *x.min(&x_min),
                    *y.min(&y_min),
                    x_max.max(x + width),
                    y_max.max(y + height),
                ]
            },
        );

        for i in y_min..y_max {
            // red border
            let col = image::Rgba::from([0xff, 0, 0, 0xff]);
            image_graph.put_pixel(x_min, i, col);
            image_graph.put_pixel(x_max - 1, i, col);
        }
        for j in x_min..x_max {
            // red bottom
            let col = image::Rgba::from([0xff, 0, 0, 0xff]);
            image_graph.put_pixel(j, y_min, col);
            image_graph.put_pixel(j, y_max - 1, col);
        }

        [x_min, y_min, x_max, y_max]
    };

    // Writing debug output (testing segmentation)
    if let Some(croppee_path) = snd_arg {
        let croppee_file = BufReader::new(
            OpenOptions::new()
                .create(false)
                .read(true)
                .open(&croppee_path)
                .unwrap(),
        );
        let (x, y, width, height) = (
            main_bound[0],
            main_bound[1],
            main_bound[2] - main_bound[0],
            main_bound[3] - main_bound[1],
        );

        let ext = croppee_path
            .rfind('.')
            .map(|i| croppee_path[i + 1..].to_lowercase());
        let im = match ext.as_ref().map(|x| x.as_str()) {
            Some("jpeg" | "jpg") => {
                ImageReader::with_format(croppee_file, image::ImageFormat::Jpeg)
                    .decode()
                    .unwrap()
            }
            Some("png") => ImageReader::with_format(croppee_file, image::ImageFormat::Png)
                .decode()
                .unwrap(),
            _ => ImageReader::new(croppee_file).decode().unwrap(),
        };
        let cropped_image = im.crop_imm(x, y, width, height);
        let ext = output_path
            .rfind('.')
            .map(|i| output_path[i + 1..].to_lowercase());
        let mut cropped_file = BufWriter::new(
            OpenOptions::new()
                .write(true)
                .create(true)
                .open(output_path)
                .unwrap(),
        );
        cropped_image
            .write_to(
                &mut cropped_file,
                match ext.as_ref().map(|x| x.as_str()) {
                    Some("jpeg") => image::ImageFormat::Jpeg,
                    Some("png") => image::ImageFormat::Png,
                    _ => image::ImageFormat::Png,
                },
            )
            .unwrap();
    } else {
        let mut sample_target = BufWriter::new(
            OpenOptions::new()
                .create(true)
                .read(true)
                .write(true)
                .open(output_path)
                .unwrap(),
        );

        image_graph
            .write_to(&mut sample_target, image::ImageFormat::Png)
            .unwrap();
    }
}
