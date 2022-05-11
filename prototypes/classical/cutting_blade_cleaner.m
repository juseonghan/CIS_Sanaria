%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% This function receives in an image and uses classical image processing
% methods to determine whether or not the cutting blade station is dirty or
% not. This is a component of the sanaria_cv_dl project, specifically the
% qa_cutting_station_clean task.

% inputs:   img_path the path to the image to read

% outputs:  classification_result the output of the classification
% algorithm

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function classification_result = cutting_blade_cleaner(img_path)
    % read in image
    img = imread(img_path);

    % convert to grayscale
    img_gray = rgb2gray(img);

    % get ROI
    height = size(img_gray, 1);
    width = size(img_gray, 2);
    
    img_roi = img_gray(1: floor(height/13), :);
    %img_roi = img_gray(1: floor(height/13), floor(width/3: 2*width/3));
    
    
    % try to isolate the mosquitos

    % get contrasted image since mosquitoes are black
    img_contrast = 255 - img_roi;
    
    % histogram equalization for better contrast
    img_eq = histeq(img_contrast, 64);

    % binarize the image from different thresholds
    [r, c] = find(img_eq == 255);
    img_bin = create_binary_img(r,c, size(img_eq));
    
    % attempt to get rid of gripper by using region growing methods
    marker = false(size(img_bin));
    marker(80:89, 920:930) = true;
    marker(90:100, 865:875) = true;
    img_gripper = imreconstruct(marker, img_bin);
    img_anti_gripper = img_bin;
    img_anti_gripper(img_gripper == 1) = 0; 
    
    % open the image for denoising
    se2 = strel('disk', 2);
    img_res = imerode(img_anti_gripper, se2);
    
    % count the number of white pixels
    area = nnz(img_res);
    
    if area > 1000
        classification_result = 1;
    else
        classification_result = 0;
    end
    
    figure;
    montage({img_roi, img_bin, img_anti_gripper, img_res}, 'Size', [4 1]);

end