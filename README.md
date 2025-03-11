# cs598-DLH
Project of CS 598 Deep Learning for Healthcare. To reproduce the paper *On the Design of Convolutional Neural Networks for Automatic Detection of Alzheimer's Disease*.

## Data preparation
1. Register ADNI dataset
   * To download the ADNI dataset you first need to register to the [LONI Image & Data Archive (IDA)](https://ida.loni.usc.edu/login.jsp), a secure research data repository, and then request access to the ADNI dataset through the submission of an [online application form](https://ida.loni.usc.edu/collaboration/access/appApply.jsp?project=ADNI).
2. Download image data and clinical data
   * Follow the [instructions](https://aramislab.paris.inria.fr/clinica/docs/public/dev/Converters/ADNI2BIDS/) to download the image data and clinical data.
   * Also follow specific requirements in the original paper [github](https://github.com/NYUMedML/CNN_design_for_AD/tree/master?tab=readme-ov-file#download-adni-data)
3. Install software
   * Install the following python (Python 3.6 or above) packages
     ```
      PyTorch 0.4
      torchvision
      progress
      matplotlib
      numpy
      visdom
     ```
   * Install miniconda, clinic, and dcm2niix
     ```
     curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o /tmp/miniconda-installer.sh
     
     bash /tmp/miniconda-installer.sh
     
     conda create --name clinicaEnv python=3.10
     
     conda activate clinicaEnv
     
     pip install clinica
     
     pip install dcm2niix
     ```
   * Install SPM and Matlab \
    If you only installed the core of Clinica, this pipeline needs the installation of either [SPM12](https://aramislab.paris.inria.fr/clinica/docs/public/dev/Software/Third-party/#spm12) and [Matlab](https://aramislab.paris.inria.fr/clinica/docs/public/dev/Software/Third-party/#matlab), or [SPM standalone](https://aramislab.paris.inria.fr/clinica/docs/public/dev/Software/Third-party/#spm12-standalone) on your computer.

4. Convert downloaded data
   ```
   clinica -v convert adni-to-bids MRI_IMAGE_DIR CLINICAL_DATA_DIR CONVERTED_OUTPUT_DIR -m T1
   ```
5. Preprocess data

