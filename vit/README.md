# README (**Submission ID: 755**)

## 1. Submission Title

**Right Time to Learn: Promoting Generalization via Bio-inspired Spacing Effect in Knowledge Distillation**



## 2. Abstract

Knowledge distillation (KD) is a powerful strategy for training deep neural networks (DNNs). While it is widely used to train a more compact “student” model from a large “teacher” model, many recent efforts have focused on finding a more effective path to improve the generalization of neural networks via KD, such as online KD and self KD. Here, we propose an easy-to-use and compatible strategy to improve the effectiveness of both online KD and self KD, inspired by a well-known paradigm for improving learning in animals and humans: spaced learning. The spacing effect is a prominent theory in the learning and memory field, demonstrating that appropriate intervals between learning trials can significantly enhance learning performance. By introducing spaced learning into online KD and self KD, we collect comprehensive empirical evidence demonstrating that Spaced KD effectively improves the learning performance of neural networks (e.g., the additional performance gain is up to 2.31% and 3.34% on Tiny-ImageNet over online KD and self KD, respectively). Furthermore, our theoretical analysis and experimental validation indicate that the benefits of the spacing effect in KD stem from seeking a flat minima in the stochastic gradient descent (SGD) process.




## 2. Spaced KD demo for ResNets under online KD and self KD

- Source code and demo instruction for online KD in folder `resnet/online_KD`

  ```sh
  cd resnet/online_KD
  ```

- Source code and demo instruction for self KD in folder `resnet/self_KD`

  ```sh
  cd resnet/self_KD
  ```

- Environment installation

  - python: 3.11.5 
    pttorch: 1.12.1+cu116
    torchvision: 0.13.1+cu116

- Other dependency and training instructions are listed in the corresponding folders.



## 3. Spaced KD demo for ViTs under online KD

- Source code in folder `vit`

   ```sh
   cd ./vit
   ```

- Environment installation
   1.  python: 3.8.12
   
       pytorch: 1.8.0
   
       cudatookit: 10.1
   
   2.  install required dependency:
   
       ```sh
       pip install -r requirements.txt
       ```
   
   3.  download datasets from their official websites and move to `vit/data` folder:
   
       - [CIFAR-100](https://www.cs.toronto.edu/~kriz/cifar.html)
       - [Tiny ImageNet](https://www.kaggle.com/c/tiny-imagenet)
   
   4.  Train from scratch (base model) of DeiT-Tiny over CIFAR-100
   
       ```sh
       python run_net.py --mode train --cfg configs/deit/deit-ti_c100_base.yaml
       ```
   
   5.  Train naive online KD of DeiT-Tiny over CIFAR-100
   
       ```sh
       python run_net.py --mode train --cfg configs/deit/deit-ti_c100_online.yaml
       ```
   
   6.  Train Spaced KD of DeiT-Tiny over CIFAR-100
   
       ```
       python run_net.py --mode train --cfg configs/deit/deit-ti_c100_space_0_5.yaml
       python run_net.py --mode train --cfg configs/deit/deit-ti_c100_space_1_0.yaml
       python run_net.py --mode train --cfg configs/deit/deit-ti_c100_space_1_5.yaml
       python run_net.py --mode train --cfg configs/deit/deit-ti_c100_space_2_0.yaml
       ```
   
   Configs of experiments of different ViT architectures and datasets are listed in `vit/configs`

