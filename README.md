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
     **Note**: The Clinica (version 0.9.3) has a bug working with SPM standalone. Please find the following Google group chat and the issue link. There is no ETA at this moment. I suggest a workaround for this bug by using Matlab and SPM12.
      * https://groups.google.com/g/clinica-user/c/kEInZhTrz0s
      * https://github.com/aramis-lab/clinica/issues/1481
   
     * To install Matlab, please follow the details in [Matlab](https://www.mathworks.com/products/matlab.html). Note that using Matlab requires having a valid license, which might be available through your university or institution.
     * To install SPM12 and Matlab, please follow the [wiki](https://en.wikibooks.org/wiki/SPM/Installation_on_64bit_Mac_OS_(Intel)#macOS_Catalina,_Big_Sur,_Monterey,_Ventura)


4. Convert downloaded data
   * Use the following command lines to convert the downloaded image data into BIDS format. Find more details on how to run clinica [convert](https://aramislab.paris.inria.fr/clinica/docs/public/dev/Converters/ADNI2BIDS/)
   ```
   conda activate clinicaEnv
   clinica -v convert adni-to-bids MRI_IMAGE_DIR CLINICAL_DATA_DIR CONVERTED_OUTPUT_DIR -m T1
   ```
5. Preprocess data
   * Use the converted BIDS data from the previous step and the function generate_split_all in script (preprocess/scripts/adni_meta_parse.py
) to generate TSV files for train/test/val dataset. Then use the following command lines to generate the train/test/val datasets. Find more details on how to run clinica [t1-volume](https://aramislab.paris.inria.fr/clinica/docs/public/dev/Pipelines/T1_Volume/)
   ```
   conda activate clinicaEnv
   export SPM_HOME="SPM_INSTALLED_PATH"
   export PATH=/Applications/MATLAB_R2019a.app/bin:$PATH
   clinica run t1-volume CONVERTED_OUTPUT_DIR ./ADNI_processed TRAIN -tsv ./ADNI_converted_meta_all/sample_30/Train_ADNI.tsv -wd './WD_train' -np 1
   clinica run t1-volume-existing-template CONVERTED_OUTPUT_DIR ./ADNI_processed TRAIN -tsv ./ADNI_converted_meta_all/sample_30/Val_ADNI.tsv -wd './WD_val' -np 1
   clinica run t1-volume-existing-template CONVERTED_OUTPUT_DIR ./ADNI_processed TRAIN -tsv ./ADNI_converted_meta_all/sample_30/Test_ADNI.tsv -wd './WD_Test' -np 1
   ```

## Model training

## Model evaluation


