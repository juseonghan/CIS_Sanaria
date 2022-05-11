%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% This function receives two column vectors of the same size which
% represents the row and column indices where a binary image = 1. The
% output creates the corresponding binary image.

% inputs:   r the row value 
%           c the column value 
%           dim the dimensions of the output image

% outputs:  res the output binary image

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function res = create_binary_img(r,c, dim) 

    res = zeros(dim, 'logical');
    for i = 1:length(r)
        res(r(i), c(i)) = 1; 
    end
end