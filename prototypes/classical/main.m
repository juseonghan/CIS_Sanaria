addpath 'data';
addpath 'result/clean';
addpath 'result/dirty';

data_dir = dir('data');
data_size = size(data_dir, 1) - 2;
images = fullfile('data', '*.png');
images = dir(images);

%res = zeros(1, data_size);
res = cutting_blade_cleaner('20220213-163212.808_pick.png')

% for i = 1:data_size
%     res(i) = cutting_blade_cleaner(images(i).name);
% end
% 
% res_dirty = find(res == 1);
% res_clean = find(res == 0);
% 
% res_dirty_imgs = []; 
% res_clean_imgs = []; 
% 
% for i = 1:length(res_dirty)
%     res_dirty_imgs = [res_dirty_imgs images(res_dirty(i)).name];
% end
% 
% for i = 1:length(res_clean)
%     res_clean_imgs = [res_clean_imgs images(res_clean(i)).name];
% end
% 
% writematrix(res_dirty_imgs, 'result/dirty_results.txt');
% writematrix(res_clean_imgs, 'result/clean_results.txt');