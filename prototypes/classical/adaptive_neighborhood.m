function [mask, result_img] = adaptive_neighborhood(img, seed)
    % 8-connectivity Region growing implementation for binary image
    
    iter = 1;
    
    while iter < 1000
        % get 3x3 matrix around seed
        eight = img(seed(1) - 1: seed(1) + 1, seed(2) -1:seed(2)+1);
        
        
        
    end
end