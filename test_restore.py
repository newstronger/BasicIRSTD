import argparse
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision.transforms import functional as F
from net import Net
from dataset import *
import matplotlib.pyplot as plt
from metrics import *
import os
import time

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
parser = argparse.ArgumentParser(description="PyTorch BasicIRSTD test")
parser.add_argument("--model_names", default='DNANet', type=str, 
                    help="model_name: 'ACM', 'ALCNet', 'DNANet', 'ISNet', 'UIUNet', 'RDIAN', 'ISTDU-Net', 'U-Net', 'RISTDnet'")
parser.add_argument("--pth_dirs", default='DNANet_70.pth.tar', type=str, help="checkpoint dir, default=None or ['NUDT-SIRST/ACM_400.pth.tar','NUAA-SIRST/ACM_400.pth.tar']")
parser.add_argument("--dataset_dir", default='./datasets', type=str, help="train_dataset_dir")
parser.add_argument("--dataset_names", default='WildIRSTD', type=str,
                    help="dataset_name: 'NUAA-SIRST', 'NUDT-SIRST', 'IRSTD-1K', 'SIRST3', 'NUDT-SIRST-Sea'")
parser.add_argument("--img_norm_cfg", default=None, type=dict,
                    help="specific a img_norm_cfg, default=None (using img_norm_cfg values of each dataset)")

parser.add_argument("--save_img", default=True, type=bool, help="save image of or not")
parser.add_argument("--save_img_dir", type=str, default='./inference/mask/', help="path of saved image")
parser.add_argument("--save_log", type=str, default='./log_seed_posSample/', help="path of saved .pth")
parser.add_argument("--threshold", type=float, default=0.5)
parser.add_argument("--batchSize", type=int, default=1, help="Training batch sizse")

global opt
opt = parser.parse_args()
if opt.save_img == True:
    opt.batchSize=1

def test(): 
    test_set = TestSetLoader(opt.dataset_dir, opt.train_dataset_name, opt.test_dataset_name, opt.img_norm_cfg)
    test_loader = DataLoader(dataset=test_set, num_workers=8, batch_size=opt.batchSize, shuffle=False)
    
    net = Net(model_name=opt.model_name, mode='test').cuda()
    net.load_state_dict(torch.load(opt.pth_dir)['state_dict'])
    net.eval()
    for idx_iter, (img, size, img_dir) in enumerate(test_loader):
        pred=img
        _,_,h,w=img.shape
        pred=Variable(pred).cuda()
        img = Variable(img).cuda().squeeze(0).unsqueeze(0)
        # pred=net.forward(img)
        for i in range(0, h, 512):
            for j in range(0,w,512):
                sub_img=img[:,:,i:i+512,j:j+512]
                sub_pred=net.forward(sub_img)
                pred[:,:,i:i+512,j:j+512]=sub_pred
        pred = pred[:,:,:size[0],:size[1]] 

        if opt.save_img == True:
            _img=(pred[0,0,:,:]>opt.threshold).float().cpu()
            img_save = transforms.ToPILImage()(_img)
            if not os.path.exists(opt.save_img_dir):
                os.makedirs(opt.save_img_dir)
            img_save.save(opt.save_img_dir + img_dir[0] + '.png')  

if __name__ == '__main__':
    opt.test_dataset_name = opt.dataset_names
    opt.model_name = opt.model_names
    opt.train_dataset_name = opt.dataset_names
    opt.pth_dir=opt.pth_dirs
    test()
        
