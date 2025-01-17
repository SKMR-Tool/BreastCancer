'''
shape, roi shape
'''
import os
import numpy as np
import matplotlib.pyplot as plt
from MeDIT.Normalize import Normalize01, NormalizeZ
from MeDIT.Visualization import Imshow3DArray
from MeDIT.ArrayProcess import ExtractBlock
from MeDIT.SaveAndLoad import LoadImage


def GetCenter(roi):
    roi = np.squeeze(roi)
    if np.ndim(roi) == 3:
        roi = roi[1]
    non_zero = np.nonzero(roi)
    center_x = int(np.median(np.unique(non_zero[1])))
    center_y = int(np.median(np.unique(non_zero[0])))
    return (center_x, center_y)


def GetCenter3D(roi):
    roi = np.squeeze(roi)

    non_zero = np.nonzero(roi)
    center_y = int(np.median(np.unique(non_zero[0])))
    center_x = int(np.median(np.unique(non_zero[1])))
    center_z = int(np.median(np.unique(non_zero[2])))
    return (center_x, center_y, center_z)



def CheckNPY():
    data_folder = r'/home/zhangyihong/Documents/BreastClassification/DCEPost/t1_post'
    max_row = []
    max_col = []
    for case in os.listdir(data_folder):
        if case == 'E054_65.npy':
            data_path = os.path.join(data_folder, case)
            data = np.load(data_path)
            cancer = np.load(os.path.join(r'/home/zhangyihong/Documents/BreastClassification/DCEPost/lesion_roi', case))
            cancer = np.clip(cancer, a_max=1, a_min=0)
            breast = np.load(os.path.join(r'/home/zhangyihong/Documents/BreastClassification/DCEPost/breast_mask', case))
            center = GetCenter(cancer)
            data_crop, _ = ExtractBlock(data, patch_size=[3, 80, 80], center_point=(-1, center[1], center[0]))
            cancer_crop, _ = ExtractBlock(cancer, patch_size=[3, 80, 80], center_point=(-1, center[1], center[0]))
            breast_crop, _ = ExtractBlock(breast, patch_size=[3, 80, 80], center_point=(-1, center[1], center[0]))
            plt.subplot(221)
            plt.imshow(data[0], cmap='gray')
            plt.subplot(222)
            plt.imshow(data[1], cmap='gray')
            plt.subplot(223)
            plt.imshow(data[2], cmap='gray')
            plt.show()

            # Imshow3DArray(Normalize01(data))

        # plt.figure(figsize=(6, 6))
        # plt.title('{}, {}'.format(np.max(np.sum(cancer_crop[1], axis=0)), np.max(np.sum(cancer_crop[1], axis=1))))
        # plt.imshow(data_crop[1], cmap='gray')
        # plt.contour(cancer_crop[1], colors='r')
        # plt.gca().set_axis_off()
        # plt.gca().xaxis.set_major_locator(plt.NullLocator())
        # plt.gca().yaxis.set_major_locator(plt.NullLocator())
        # plt.savefig(os.path.join(r'/home/zhangyihong/Documents/BreastClassification/DCEPost/image', '{}.jpg').
        #             format(case[: case.index(('.npy'))]), bbox_inches='tight', pad_inches=0.0)
        # plt.close()
        # max_col.append(np.max(np.sum(cancer_crop[1], axis=(0))))
        # max_row.append(np.max(np.sum(cancer_crop[1], axis=(1))))
    # print(max(max_col), max(max_row))
# CheckNPY()


def Normalize():
    data_folder = r'/home/zhangyihong/Documents/BreastClassification/DCEPost/lesion_roi'
    new_folder = r'/home/zhangyihong/Documents/BreastClassification/DCEPost/lesion_roi_norm'
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
    for case in os.listdir(data_folder):
        # print(case)
        data_path = os.path.join(data_folder, case)
        data = np.load(data_path)
        data = np.clip(data, a_min=0., a_max=1.)
        # data = NormalizeZ(data)
        if (np.unique(data) != np.array([0., 1.], dtype=np.float32)).all():
            print(case, np.unique(data))
        np.save(os.path.join(new_folder, case), data)
# Normalize()


def CropData():
    data_folder = r'/home/zhangyihong/Documents/BreastClassification/DCEPost/t1_post'
    new_folder = r'/home/zhangyihong/Documents/BreastClassification/DCEPost/t1_post_crop_norm'
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
    for case in os.listdir(data_folder):
        data_path = os.path.join(data_folder, case)
        data = np.load(data_path)
        cancer = np.load(os.path.join(r'/home/zhangyihong/Documents/BreastClassification/DCEPost/lesion_roi_norm', case))
        center = GetCenter(cancer)
        data_crop, _ = ExtractBlock(data, patch_size=[3, 100, 100], center_point=(-1, center[1], center[0]))
        np.save(os.path.join(new_folder, case), NormalizeZ(data))
        # plt.imshow(data_crop[1], cmap='gray')
        # plt.show()
# CropData()



def CropROI():
    data_folder = r'/home/zhangyihong/Documents/BreastClassification/DCEPost/lesion_roi_norm'
    new_folder = r'/home/zhangyihong/Documents/BreastClassification/DCEPost/lesion_roi_crop_norm'
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
    for case in os.listdir(data_folder):
        cancer = np.load(os.path.join(r'/home/zhangyihong/Documents/BreastClassification/DCEPost/lesion_roi_norm', case))
        center = GetCenter(cancer)
        cancer_crop, _ = ExtractBlock(cancer, patch_size=[3, 100, 100], center_point=(-1, center[1], center[0]))
        np.save(os.path.join(new_folder, case), cancer_crop)
# CropROI()



def Statistical():
    data_folder = r'V:\jzhang\breastFormatNew'
    for case in os.listdir(data_folder):
        case_folder = os.path.join(data_folder, case)
        if not os.path.isdir(case_folder):
            continue
        else:
            '''ESER_1.nii.gz, ADC_Reg.nii.gz, t2_W_Reg.nii.gz.....roi3D.nii'''
            eser, _, _ = LoadImage(os.path.join(case_folder, 'ESER_1.nii.gz'), is_show_info=False)
            adc, _, _ = LoadImage(os.path.join(case_folder, 'ADC_Reg.nii.gz'), is_show_info=False)
            t2_W, _, _ = LoadImage(os.path.join(case_folder, 't2_W_Reg.nii.gz'), is_show_info=False)
            roi, _, _ = LoadImage(os.path.join(case_folder, 'roi3D.nii'), is_show_info=False)
            if not (eser.GetSize() == adc.GetSize() == t2_W.GetSize() == roi.GetSize()):
                print('Size: {}'.format(case))
            # if not (eser.GetDirection() == adc.GetDirection() == t2_W.GetDirection() == roi.GetDirection()):
            #     print('Direction: {}'.format(case))
            if not (eser.GetSpacing() == adc.GetSpacing() == t2_W.GetSpacing() == roi.GetSpacing()):
                print('Spacing: {}'.format(case))
            if not (eser.GetOrigin() == adc.GetOrigin() == t2_W.GetOrigin() == roi.GetOrigin()):
                print('Origin: {}'.format(case))
# Statistical()


def StatisticalSpacing():
    data_folder = r'V:\jzhang\breastFormatNew'
    for case in os.listdir(data_folder):
        case_folder = os.path.join(data_folder, case)
        if not os.path.isdir(case_folder):
            continue
        else:
            '''ESER_1.nii.gz, ADC_Reg.nii.gz, t2_W_Reg.nii.gz.....roi3D.nii'''
            eser, _, _ = LoadImage(os.path.join(case_folder, 'ESER_1.nii.gz'), is_show_info=False)
            print('{} {}'.format(eser.GetSpacing(), case))

# StatisticalSpacing()


def LoadData(type_list):
    ''' ESER_1.nii.gz, ADC_Reg.nii.gz, t2_W_Reg.nii.gz.....roi3D.nii '''

    data_folder = r'\\mega\\homesall\jzhang\breastFormatNew'

    for case in os.listdir(data_folder):
        case_folder = os.path.join(data_folder, case)
        if not os.path.isdir(case_folder):
            continue
        else:
            image_list, data_list = [], []
            for data_type in type_list:
                image, data, _ = LoadImage(os.path.join(case_folder, data_type), is_show_info=False)
                image_list.append(image)
                data_list.append(data)
            yield case, image_list, data_list


def Shape():
    slice_list = []
    height_list = []
    width_list = []
    case_list = []
    for case, image, data in LoadData('roi3D.nii'):
        # if case != 'A191_GE CHUN YIN':
        #     continue
        height = list(sorted(set(np.nonzero(data)[0])))
        width = list(sorted(set(np.nonzero(data)[1])))
        slice = list(sorted(set(np.nonzero(data)[2])))

        height_list.append(height[-1] - height[0])
        width_list.append(width[-1] - width[0])
        slice_list.append(slice[-1] - slice[0])
        case_list.append(case)
    print(sorted(slice_list))
    print(sorted(height_list))
    print(sorted(width_list))
    # print(case_list[slice_list.index(max(slice_list))],
    #       case_list[height_list.index(max(height_list))],
    #       case_list[width_list.index(max(width_list))])
    print()
# Shape()


def TestCrop():
    for case, image_list, data_list in LoadData(['roi3D.nii']):
        image = image_list[0]
        data = data_list[0]
        x, y, z = GetCenter3D(data)
        plt.imshow(data[..., z], cmap='gray')
        plt.scatter(x, y)
        plt.show()
# TestCrop()


def CropData3D():
    from MeDIT.ArrayProcess import ExtractBlock
    from MeDIT.Normalize import NormalizeZ
    os.mkdir(r'\\mega\\homesall\jzhang\BreastProject\BreastNpyCorrect\dwi_b50')
    os.mkdir(r'\\mega\\homesall\jzhang\BreastProject\BreastNpyCorrect\e_peak_1')
    os.mkdir(r'\\mega\\homesall\jzhang\BreastProject\BreastNpyCorrect\msi_1')
    os.mkdir(r'\\mega\\homesall\jzhang\BreastProject\BreastNpyCorrect\sep_1')
    os.mkdir(r'\\mega\\homesall\jzhang\BreastProject\BreastNpyCorrect\si_slope_1')
    os.mkdir(r'\\mega\\homesall\jzhang\BreastProject\BreastNpyCorrect\t1_peak_reset')
    os.mkdir(r'\\mega\\homesall\jzhang\BreastProject\BreastNpyCorrect\t1_pre_reset')
    for case, image_list, data_list in LoadData(['dwi_b50_Reg.nii.gz', 'e_peak_1.nii.gz', 'msi_1.nii.gz',
                                                 'sep_1.nii.gz', 'si_slope_1.nii.gz',
                                                 't1_peak_reset.nii.gz', 't1_pre_reset.nii.gz',
                                                 'roi3D.nii']):
        print(case)
        dwi_b50 = data_list[0]
        e_peak_1 = data_list[1]
        msi_1 = data_list[2]
        sep_1 = data_list[3]
        si_slope_1 = data_list[0]
        t1_peak_reset = data_list[1]
        t1_pre_reset = data_list[2]

        roi = data_list[-1]
        x, y, z = GetCenter3D(roi)
        crop_dwi_b50, _ = ExtractBlock(dwi_b50, (100, 100, 50), center_point=(y, x, z), is_shift=True)
        crop_e_peak_1, _ = ExtractBlock(e_peak_1, (100, 100, 50), center_point=(y, x, z), is_shift=True)
        crop_msi_1, _ = ExtractBlock(msi_1, (100, 100, 50), center_point=(y, x, z), is_shift=True)
        crop_sep_1, _ = ExtractBlock(sep_1, (100, 100, 50), center_point=(y, x, z), is_shift=True)
        crop_si_slope_1, _ = ExtractBlock(si_slope_1, (100, 100, 50), center_point=(y, x, z), is_shift=True)
        crop_t1_peak_reset, _ = ExtractBlock(t1_peak_reset, (100, 100, 50), center_point=(y, x, z), is_shift=True)
        crop_t1_pre_reset, _ = ExtractBlock(t1_pre_reset, (100, 100, 50), center_point=(y, x, z), is_shift=True)


        crop_dwi_b50 = crop_dwi_b50.transpose((2, 0, 1))
        crop_e_peak_1 = crop_e_peak_1.transpose((2, 0, 1))
        crop_msi_1 = crop_msi_1.transpose((2, 0, 1))
        crop_sep_1 = crop_sep_1.transpose((2, 0, 1))
        crop_si_slope_1 = crop_si_slope_1.transpose((2, 0, 1))
        crop_t1_peak_reset = crop_t1_peak_reset.transpose((2, 0, 1))
        crop_t1_pre_reset = crop_t1_pre_reset.transpose((2, 0, 1))

        np.save(os.path.join(r'\\mega\\homesall\jzhang\BreastProject\BreastNpyCorrect\dwi_b50', '{}.npy'.format(case)), NormalizeZ(crop_dwi_b50))
        np.save(os.path.join(r'\\mega\\homesall\jzhang\BreastProject\BreastNpyCorrect\e_peak_1', '{}.npy'.format(case)), NormalizeZ(crop_e_peak_1))
        np.save(os.path.join(r'\\mega\\homesall\jzhang\BreastProject\BreastNpyCorrect\msi_1', '{}.npy'.format(case)), NormalizeZ(crop_msi_1))
        np.save(os.path.join(r'\\mega\\homesall\jzhang\BreastProject\BreastNpyCorrect\sep_1', '{}.npy'.format(case)), NormalizeZ(crop_sep_1))
        np.save(os.path.join(r'\\mega\\homesall\jzhang\BreastProject\BreastNpyCorrect\si_slope_1', '{}.npy'.format(case)), NormalizeZ(crop_si_slope_1))
        np.save(os.path.join(r'\\mega\\homesall\jzhang\BreastProject\BreastNpyCorrect\t1_peak_reset', '{}.npy'.format(case)), NormalizeZ(crop_t1_peak_reset))
        np.save(os.path.join(r'\\mega\\homesall\jzhang\BreastProject\BreastNpyCorrect\t1_pre_reset', '{}.npy'.format(case)), NormalizeZ(crop_t1_pre_reset))

CropData3D()


# from MeDIT.Visualization import FlattenImages
# for case in os.listdir(r'/home/zhangyihong/Documents/BreastNpy/T1WI_pos'):
#     # data = np.load(os.path.join(r'Y:\BreastNPYCorrect\T1WI_pos', case))
#     data = np.load(os.path.join(r'/home/zhangyihong/Documents/BreastNpy/T1WI_pos', case))
#     roi = np.load(os.path.join(r'/home/zhangyihong/Documents/BreastNpy/RoiDilated', case))
#     flatten_data = FlattenImages(data)
#     flatten_roi = FlattenImages(roi)
#     # flatten_data = FlattenImages(np.transpose(data, axes=(2, 0, 1)))
#     # flatten_roi = FlattenImages(np.transpose(roi, axes=(2, 0, 1)))
#
#     plt.figure(figsize=(16, 16))
#     plt.imshow(flatten_data, cmap='gray')
#     plt.contour(flatten_roi, colors='r')
#     plt.axis('off')
#     plt.show()
    # plt.savefig(os.path.join(r'V:\yhzhang\BreastNpy\Image', '{}.jpg'.format(case.split('.npy')[0])))
    # plt.close()