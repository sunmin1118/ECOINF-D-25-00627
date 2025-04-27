import os
from PIL import Image
from tqdm import tqdm
from module_def import Unet
from utils.utils_metrics import compute_mIoU, show_results
if __name__ == "__main__":
    miou_mode       = 0
    num_classes     = 8
    name_classes = ["_background_","Platanus","Cinnamomum","Ginkgo","Sapindaceae","Cedrus","Salix","Metasequoia"]
    VOCdevkit_path  = 'voc_path'
    image_ids       = open(os.path.join(VOCdevkit_path, "val.txt"),'r').read().splitlines()
    gt_dir          = os.path.join(VOCdevkit_path, "[set_data_path]")
    miou_out_path   = "miou_out"
    pred_dir        = os.path.join(miou_out_path, 'detection-results')

    if miou_mode == 0 or miou_mode == 1:
        if not os.path.exists(pred_dir):
            os.makedirs(pred_dir)
            
        print("Load model.")
        unet = Unet()
        print("Load model done.")

        print("Get predict result.")
        for image_id in tqdm(image_ids):
            image_path  = os.path.join(VOCdevkit_path, "[dateset_path]"+image_id+".png")
            image       = Image.open(image_path)
            image       = unet.get_miou_png(image)
            image.save(os.path.join(pred_dir, image_id + ".png"))
        print("Get predict result done.")

    if miou_mode == 0 or miou_mode == 2:
        print("Get miou.")
        hist, IoUs, PA_Recall, Precision = compute_mIoU(gt_dir, pred_dir, image_ids, num_classes, name_classes)  # 执行计算mIoU的函数
        print("Get miou done.")
        show_results(miou_out_path, hist, IoUs, PA_Recall, Precision, name_classes)