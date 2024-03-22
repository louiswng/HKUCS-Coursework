source_image_path=img/source.png
target_image_path=img/target.png
mask_path=img/mask.png
result_image_path=img/result.png

python main.py \
    --src_img ${source_image_path} \
    --tgt_img ${target_image_path} \
    --mask_img ${mask_path} \
    --res_img ${result_image_path} \
