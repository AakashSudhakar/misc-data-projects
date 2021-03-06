"""
NAME:               svm_MLiA.py (data_projects/machine_learning_in_action/algo_ch06/)

DESCRIPTION:        Python class application of the support vector machine algorithm.

                    The support vector machine is a probability-based decision machine
                    designed to classify data by using support vectors (data values near
                    the data's line-of-best-fit) to accurately project regressional
                    relationships and classify new data in a memory-efficient manner.

                    All source code is available at www.manning.com/MachineLearningInAction. 

USE CASE(S):        Numeric and nominal values

ADVANTAGE(S):       Computationally cheap
                    Relatively low generalization error
                    Easy to contextually understand learned results

DISADVANTAGE(S):    Natively only handles binary classification
                    Sensitive to tuning parameters and choice of kernel

NOTE:               The handwriting application of SVM requires a subdirectory of images called 
                    'digits' that is too large to upload to GitHub. Instead, download and unpack
                    the file titled 'digits.zip'.

                    Original source code is in Python 2, but my code is in Python 3.

CREDIT:             Machine Learning in Action (Peter Harrington)
"""


# ====================================================================================
# ================================ IMPORT STATEMENTS =================================
# ====================================================================================


import sys                                  # Library for interpreter system flexibility
import numpy as np                          # Library for simple linear mathematical operations
from os import listdir as ld                # Package for returning list of directory filenames
from time import time as t                  # Package for tracking modular and program runtime


# ====================================================================================
# ===================== CLASS DEFINITION: SUPPORT VECTOR MACHINE =====================
# ====================================================================================


# TODO: Create algorithm copy in separate file for handwriting images example
class Support_Vector_Machine_Algorithm(object):

    # ======================== CLASS INITIALIZERS/DECLARATIONS =======================
    def __init__(self, TIME_I):
        self.TIME_I = TIME_I                            # Initial time measure for runtime tracker
        # TODO: Uncomment line below once handwriting example is refactored into new file
        # self.FILE = open("sample_test_set.txt")       # Open filename as read-only for test dataset

    # ======================== METHOD TO LOAD IN SAMPLE DATASET ======================
    def load_dataset(self, filename):
        FILE = open(filename)
        dataset = []
        labels = []

        # Iterates through sample file to produce sample dataset and class label vector
        for line in FILE.readlines():
            array_of_lines = line.strip().split("\t")
            dataset.append([float(array_of_lines[0]), float(array_of_lines[1])])
            labels.append(float(array_of_lines[2]))

        """ print("\nSAMPLE DATASET IS: \n{}\n\nSAMPLE LABELS ARE: \n{}\n".format(dataset, labels)) """
        return dataset, labels

    # ========== METHOD TO SELECT POTENTIAL ALPHA FROM UNIFORM DISTRIBUTION ==========
    def select_random_potential_alpha(self, alpha_index, alpha_total):
        potential_alpha = alpha_index

        # Produces potential alpha values while they match alpha index values
        while (potential_alpha == alpha_index):
            potential_alpha = int(np.random.uniform(0, alpha_total))
        
        """ print("\nPOTENTIAL ALPHA VALUE IS: {}\n".format(potential_alpha)) """
        return potential_alpha

    # ===== METHOD TO PROCESS POTENTIAL ALPHA VALUE AGAINST BOUNDARY CONSTRAINTS =====
    def process_alpha_against_constraints(self, alpha_from_potential, alpha_ceiling, alpha_floor):
        # Processes alpha value against ceiling constraint (cannot be greater than)
        if alpha_from_potential > alpha_ceiling:
            alpha_from_potential = alpha_ceiling

        # Processes alpha value against floor constraint (cannot be less than)
        if alpha_floor > alpha_from_potential:
            alpha_from_potential = alpha_floor

        """ print("\nALPHA VALUE PROCESSED AGAINST CONSTRAINTS IS: {}\n".format(alpha_from_potential)) """
        return alpha_from_potential

    # ========= METHOD TO TRANSFORM DATA DISTRIBUTION FROM VECTOR TO SCALAR ==========
    # =========== USING LINEAR KERNELS AND GAUSSIAN RADIAL BIAS FUNCTIONS ============
    def kernel_transformation_linear_RBF(self, dataset, data_subset, kernel_tuple):
        NUM_ROWS, NUM_COLS = np.shape(dataset)
        kernel = np.mat(np.zeros((NUM_ROWS, 1)))
        kernel_classes = ["LINEAR", "GAUSSIAN RADIAL BIAS FUNCTION", "UNKNOWN"]

        # Classifies kernel type based on tuple property value
        if kernel_tuple[0] == "lin":
            kernel_type = kernel_classes[0]
        elif kernel_tuple[0] == "rbf":
            kernel_type = kernel_classes[1]
        else:
            kernel_type = kernel_classes[2]

        # Checks kernel type and transforms kernel contextually
        if kernel_type == kernel_classes[0]:
            # Transforms linear kernel
            kernel = dataset * data_subset.T 
        elif kernel_type == kernel_classes[1]:
            # Iterates through dataset size to create kernel spread
            for iterator in range(NUM_ROWS):
                delta_rows = dataset[iterator, :] - data_subset
                kernel[iterator] = delta_rows * delta_rows.T

            # Transforms Gaussian radial bias function
            kernel = np.exp(kernel / (-1 * kernel_tuple[1] ** 2))
        else:
            # Raises error if kernel type is not linear or RBF
            raise NameError("\nKERNEL NOT RECOGNIZED OR OF BAD TYPE.\n")

        """ print("KERNEL TYPE IS: {}\n\nKERNEL IS: \n{}\n".format(kernel_type, kernel)) """
        return kernel

    # ============== METHOD TO TEST KERNEL DATA TRANSFORMATION AGAINST A =============
    # ====================== RADIAL BIAS FUNCTIONAL DISTRIBUTION =====================
    def test_kernel_transform_against_rbf(self, KERNEL_CONSTANT = 1.3):
        # Loads training data, class label vectors, and values for beta and alphas
        training_dataset, training_labels = self.load_dataset("./training_set_RBF.txt")
        beta, alphas = self.outer_loop_heuristic_smo_optimization(training_dataset, training_labels, 200, 0.0001, 10000, ("rbf", KERNEL_CONSTANT))
        
        # Produces formatted matrices for training data and class label vectors
        training_data_mat = np.mat(training_dataset)
        training_label_mat = np.mat(training_labels).transpose()

        # Produces support vectors and conditional SV information for training data
        support_vector_indices = np.nonzero(alphas.A > 0)[0]
        support_vector_mat = training_data_mat[support_vector_indices]
        support_vector_labels = training_label_mat[support_vector_indices]
        print("\nTHERE ARE {} SUPPORT VECTORS FOR OUR DATASET.\n".format(np.shape(support_vector_mat)[0]))

        # Defines training data's dimensionality constants and initializes training error
        TRAINING_NUM_ROWS, TRAINING_NUM_COLS = np.shape(training_data_mat)
        training_error_count = 0.0

        # Iterates over training dataset's length to evaluate and transform kernel data and then write predictions using support vectors
        for iterator in range(TRAINING_NUM_ROWS):
            training_kernel_evaluation = self.kernel_transformation_linear_RBF(support_vector_mat, training_data_mat[iterator, :], ("rbf", KERNEL_CONSTANT))
            training_prediction = training_kernel_evaluation.T * np.multiply(support_vector_labels, alphas[support_vector_indices]) + beta

            # Increments training error count for every data prediction mismatch
            if np.sign(training_prediction) != np.sign(training_labels[iterator]):
                training_error_count += 1.0

        # Calculates training error rate over kernel transformation
        training_error_rate = training_error_count / TRAINING_NUM_ROWS
        print("THE TRAINING ERROR RATE FOR PREDICTING FROM THE RBF KERNEL DATA IS: {}\n".format(training_error_rate))

        # Loads test data and class label vectors
        test_dataset, test_labels = self.load_dataset("./test_set_RBF.txt")
        
        # Produces formatted matrices for test data and class label vectors
        test_data_mat = np.mat(test_dataset)
        test_label_mat = np.mat(test_labels).transpose()

        # Defines test data's dimensionality constants and initializes test error
        TEST_NUM_ROWS, TEST_NUM_COLS = np.shape(test_data_mat)
        test_error_count = 0.0

        # Iterates over test dataset's length to evaluate and transform kernel data and then write predictions using support vectors
        for iterator in range(TEST_NUM_ROWS):
            test_kernel_evaluation = self.kernel_transformation_linear_RBF(support_vector_mat, test_data_mat[iterator, :], ("rbf", KERNEL_CONSTANT))
            test_prediction = test_kernel_evaluation.T * np.multiply(support_vector_labels, alphas[support_vector_indices]) + beta

            # Increments test error count for every data prediction mismatch
            if np.sign(test_prediction) != np.sign(test_labels[iterator]):
                test_error_count += 1.0

        # Calculates test error rate over kernel transformation
        test_error_rate = test_error_count / TEST_NUM_ROWS
        print("THE TEST ERROR RATE FOR PREDICTING FROM THE RBF KERNEL DATA IS: {}\n".format(test_error_rate))
        
        # Performs runtime tracker for particular method
        return self.track_runtime()

        # ========== METHOD THAT CONVERTS IMAGE TO VECTOR (FROM kNN CLASSIFIER) ==========
    def convert_image_to_vector(self, path_to_file):
        image_vector = np.zeros((1, 1024))
        IMAGE = open(path_to_file)

        # Converts 32x32 image to 1x1024 vector
        for iterator_outer in range(32):
            line = IMAGE.readline()

            for iterator_inner in range(32):
                image_vector[0, 32 * iterator_outer + iterator_inner] = int(line[iterator_inner])

        """ print("SAMPLE IMAGE VECTOR, FIRST 32 DIGITS: \n{}.\nSAMPLE IMAGE VECTOR, SECOND 32 DIGITS: \n{}.\n".format(image_vector[0, 0:31], image_vector[0, 32:63])) """
        return image_vector

    # ==== METHOD THAT LOADS IMAGES INTO DATASET AND LABELS (FROM kNN CLASSIFIER) ====
    def load_images_from_directory(self, dirname):
        # Initializes dataset, class label vector, and data's dimensionality constant
        handwriting_labels = []
        training_file_list = ld(dirname)
        DIR_LENGTH = len(training_file_list)
        training_mat = np.zeros((DIR_LENGTH, 1024))

        # Iterates through data's length to log every image file and class label
        for iterator in range(DIR_LENGTH):
            filename = training_file_list[iterator]
            file = filename.split(".")[0]
            class_number = int(file.split("_")[0])

            # Contextually labels every image by class number (provided in dataset)
            if class_number == 9:
                handwriting_labels.append(-1)
            else:
                handwriting_labels.append(1)

            # Converts training image data to information vector
            training_mat[iterator, :] = self.convert_image_to_vector("{}/{}".format(dirname, filename))
        
        print("\nTRAINING DATA MATRIX IS: \n{}\n\nHANDWRITING IMAGE LABEL VECTOR IS: \n{}\n".format(training_mat, handwriting_labels))
        return training_mat, handwriting_labels

    def test_handwriting_digits_with_advanced_svm(self, kernel_tuple = ("rbf", 10)):
        # Loads training data, class label vectors, and values for beta and alphas
        training_dataset, training_labels = self.load_images_from_directory("digits/training_digits/")
        beta, alphas = self.outer_loop_heuristic_smo_optimization(training_dataset, training_labels, 200, 0.0001, 10000, kernel_tuple)

        # Produces formatted matrices for training data and class label vectors
        training_data_mat = np.mat(training_dataset)
        training_label_mat = np.mat(training_labels).transpose()

        # Produces support vectors and conditional SV information for training data
        support_vector_indices = np.nonzero(alphas.A > 0)[0]
        support_vector_mat = training_data_mat[support_vector_indices]
        support_vector_labels = training_label_mat[support_vector_indices]
        print("\nTHERE ARE {} SUPPORT VECTORS FOR THE HANDWRITING IMAGES DATASET.\n".format(np.shape(support_vector_mat)[0]))

        # Defines test data's dimensionality constants and initializes test error
        TRAINING_NUM_ROWS, TRAINING_NUM_COLS = np.shape(training_data_mat)
        training_error_count = 0.0

        # Iterates over training dataset's length to evaluate and transform kernel data and then write predictions using support vectors
        for iterator in range(TRAINING_NUM_ROWS):
            training_kernel_evaluation = self.kernel_transformation_linear_RBF(support_vector_mat, training_data_mat[iterator, :], kernel_tuple)
            training_prediction = training_kernel_evaluation.T * np.multiply(support_vector_labels, alphas[support_vector_indices]) + beta

            # Increments test error count for every data prediction mismatch
            if np.sign(training_prediction) != np.sign(training_labels[iterator]):
                training_error_count += 1.0

        # Calculates training error rate over kernel transformation
        training_error_rate = training_error_count / TRAINING_NUM_ROWS
        print("\nTHE TRAINING ERROR RATE FOR PREDICTING FROM THE RBF KERNEL OF THE HANDWRITING IMAGES DATASET IS: {}\n".format(training_error_rate))

        # Loads test data and class label vectors
        test_dataset, test_labels = self.load_images_from_directory("digits/test_digits/")

        # Produces formatted matrices for test data and class label vectors
        test_data_mat = np.mat(test_dataset)
        test_label_mat = np.mat(test_labels).transpose()

        # Defines test data's dimensionality constants and initializes test error
        TEST_NUM_ROWS, TEST_NUM_COLS = np.shape(test_data_mat)
        test_error_count = 0.0

        # Iterates over test dataset's length to evaluate and transform kernel data and then write predictions using support vectors
        for iterator in range(TEST_NUM_ROWS):
            test_kernel_evaluation = self.kernel_transformation_linear_RBF(support_vector_mat, test_data_mat[iterator, :], kernel_tuple)
            test_prediction = test_kernel_evaluation.T * np.multiply(support_vector_labels, alphas[support_vector_indices]) + beta

            # Increments test error count for every data prediction mismatch
            if np.sign(test_prediction) != np.sign(test_labels[iterator]):
                test_error_count += 1.0

        # Calculates test error rate over kernel transformation
        test_error_rate = test_error_count / TEST_NUM_ROWS
        print("\nTHE TEST ERROR RATE FOR PREDICTING FROM THE RBF KERNEL OF THE HANDWRITING IMAGES DATASET IS: {}\n".format(test_error_rate))

        # Performs runtime tracker for particular method
        return self.track_runtime()

    # ============= METHOD TO CALCULATE POTENTIAL ALPHA RANGE VALUES BY A ============
    # ============== SIMPLE PLATT SEQUENTIAL MINIMAL OPTIMIZATION (SMO) ==============
    def simple_sequential_minimal_optimization(self, input_dataset, class_labels, absolute_ceiling_constant, alpha_tolerance, MAX_ITER):
        dataset = np.mat(input_dataset)                     # Produces formatted dataset
        labels = np.mat(class_labels).transpose()           # Produces transposed class label vector
        NUM_ROWS, NUM_COLS = np.shape(dataset)              # Produces constants of dataset's dimensionality
        beta = 0                                            # Initializes value of beta to increment later

        # Initializes alpha matrix of zeros by number of rows in dataset
        alphas = np.mat(np.zeros((NUM_ROWS, 1)))
        iteration_constant = 0

        # Iterates until predefined iteration constant and iteration ceiling are equal
        while (iteration_constant < MAX_ITER):
            changed_alpha_pairs = 0                         # Initializes dynamic alpha pair values to change later

            # Iterates based on number of rows in dataset to optimize alpha pairs
            for iterator in range(NUM_ROWS):
                # Creates temporary constants for alpha ranges against dataset and labels by the method's parent iterator
                fX_iterator = float(np.multiply(alphas, labels).T * (dataset * dataset[iterator, :].T)) + beta
                E_iterator = fX_iterator - float(labels[iterator])

                # Checks if iteration constants abide by absolute and relative boundary conditions defined by the ceiling and tolerance levels
                if ((labels[iterator] * E_iterator < -alpha_tolerance) and (alphas[iterator] < absolute_ceiling_constant)) or ((labels[iterator] * E_iterator > alpha_tolerance) and (alphas[iterator] > 0)):
                    # Creates potential alpha value from randomizer method
                    potential_alpha = self.select_random_potential_alpha(iterator, NUM_ROWS)
                    
                    # Creates temporary constants for alpha ranges against dataset and labels by the method's potential alpha ranges
                    fX_potential = float(np.multiply(alphas, labels).T * (dataset * dataset[potential_alpha, :].T)) + beta
                    E_potential = fX_potential - float(labels[potential_alpha])

                    # Creates dummy constants to hold old alpha values from method's parent iterator and potential alpha values
                    old_alpha_iterator = np.copy(alphas[iterator])
                    old_alpha_potential = np.copy(alphas[potential_alpha])

                    # Checks if iterated labels match the expected potential alpha label values
                    if (labels[iterator] != labels[potential_alpha]):
                        # Defines the alpha's ceiling and floor if there is a mismatch
                        alpha_ceiling = min(absolute_ceiling_constant, absolute_ceiling_constant + alphas[potential_alpha] - alphas[iterator])
                        alpha_floor = max(0, alphas[potential_alpha] - alphas[iterator])
                    else:
                        # Defines the alpha's ceiling and floor if there is a match
                        alpha_ceiling = min(absolute_ceiling_constant, alphas[potential_alpha] + alphas[iterator])
                        alpha_floor = max(0, alphas[potential_alpha] + alphas[iterator] - absolute_ceiling_constant)

                    # Checks if floor and ceiling are equivalent and if so, prints for convenience
                    if alpha_ceiling == alpha_floor:
                        """ print("\nFOR ALPHA'S BOUNDARY CONSTRAINTS, THE CEILING AND FLOOR ARE FOUND TO BE EQUAL.\n") """
                        continue

                    # Defines marker value for altering the alpha value for optimization
                    optimal_alpha_change_marker = 2.0 * dataset[iterator, :] * dataset[potential_alpha, :].T - dataset[iterator, :] * dataset[iterator, :].T - dataset[potential_alpha, :] * dataset[potential_alpha, :].T

                    # Checks if optimal alpha marker is zero and if so, prints for convenience
                    if optimal_alpha_change_marker >= 0:
                        """ print("\nFOR ALPHA'S OPTIMIZATION, THE VALUE OF THE OPTIMAL ALPHA CHANGE MARKER IS EQUAL TO OR GREATER THAN ZERO.\n") """
                        continue

                    # Optimizes alpha values based on optimal marker and constraint processing method
                    alphas[potential_alpha] -= labels[potential_alpha] * (E_iterator - E_potential) / optimal_alpha_change_marker
                    alphas[potential_alpha] = self.process_alpha_against_constraints(alphas[potential_alpha], alpha_ceiling, alpha_floor)

                    # Checks if margin between new and old alphas are too small and if so, prints for convenience
                    if (abs(alphas[potential_alpha] - old_alpha_potential) < 0.00001):
                        """ print("\nTHE POTENTIAL ALPHA VALUE IS NOT MOVING ENOUGH.\n") """
                        continue

                    # Increments new alpha values and produces temporary beta-values to track differential alpha changes
                    alphas[iterator] += labels[potential_alpha] * labels[iterator] * (old_alpha_potential - alphas[potential_alpha])
                    beta1 = beta - E_iterator - labels[iterator] * (alphas[iterator] - old_alpha_iterator) * dataset[iterator, :] * dataset[iterator, :].T - labels[potential_alpha] * (alphas[potential_alpha] - old_alpha_potential) * dataset[iterator, :] * dataset[potential_alpha, :].T
                    beta2 = beta - E_potential - labels[iterator] * (alphas[iterator] - old_alpha_iterator) * dataset[iterator, :] * dataset[potential_alpha, :].T - labels[potential_alpha] * (alphas[potential_alpha] - old_alpha_potential) * dataset[potential_alpha, :] * dataset[potential_alpha, :].T

                    # Checks if new alpha values fall within beta-dependent boundary conditions for beta-value reinitialization
                    if (0 < alphas[iterator]) and (absolute_ceiling_constant > alphas[iterator]):
                        beta = beta1
                    elif (0 < alphas[potential_alpha]) and (absolute_ceiling_constant > alphas[potential_alpha]):
                        beta = beta2
                    else:
                        beta = (beta1 + beta2) / 2.0

                    # Iterate dynamic alpha pair value for loop functionality
                    changed_alpha_pairs += 1
                    """ print("\nITERATION CONSTANT IS: {}\n\nFUNCTIONAL ITERATOR IS: {}\n\nCHANGED ALPHA PAIRS ARE: \n{}\n".format(iteration_constant, iterator, changed_alpha_pairs)) """

            # Checks value of dynamic alpha pair value to iterate the method's parent iteration constant
            if (changed_alpha_pairs == 0):
                iteration_constant += 1
            else:
                iteration_constant = 0
            
            # Prints formatted iteration number for method
            """ print("\nTOTAL ITERATION NUMBER IS: {}\n".format(iteration_constant)) """

        # Get number of support vectors across SVM-SMO
        print("SUPPORT VECTORS ALONG THE SAMPLE DATASET ARE:")
        [print(dataset[iterator], labels[iterator]) for iterator in range(100) if alphas[iterator] > 0.0]

        # Prints beta-values and formatted alphas greater than zero
        print("\nBETA-VALUE IS: {}\n\nALPHAS (GREATER THAN ZERO) ARE: \n{}\n".format(beta, alphas[alphas > 0]))

        """
        # Performs runtime tracker for particular method
        self.track_runtime()
        """

        return beta, alphas

    # =========== METHOD TO CALCULATE E PARAMETER FOR SVM SMO OPTIMIZATION ===========
    def calculate_E_parameter(self, smo_support_optimizer, alpha_param):
        """
        # Produces temporary holding SMO optimization parameter (NOTE: No kernel transformation)
        fX_param = float(np.multiply(smo_support_optimizer.alphas, smo_support_optimizer.labels).T * (smo_support_optimizer.dataset * smo_support_optimizer.dataset[alpha_param, :].T)) + smo_support_optimizer.beta
        """

        # Produces temporary holding SMO optimization parameter (NOTE: Kernel transformation)
        fX_param = float(np.multiply(smo_support_optimizer.alphas, smo_support_optimizer.labels).T * smo_support_optimizer.kernel[:, alpha_param] + smo_support_optimizer.beta)
        # Calculates E-parameter from temporary holding SMO optimization parameters
        E_param = fX_param - float(smo_support_optimizer.labels[alpha_param])
        
        """ print("FIRST TEMPORARY HOLDING SMO OPTIMIZATION PARAMETER fX IS: {}\n\nSECOND SMO OPTIMIZATION PARAMETER E IS: {}\n".format(fX_param, E_param)) """
        return E_param

    # ====== METHOD TO SELECT OPTIMIZED ALPHA FROM SMO OPTIMIZER AND PARAMETERS ======
    # ==================== VIA AN INNER-LOOP ITERATION HEURISTIC =====================
    def inner_loop_heuristic_smo_optimization(self, iterator, smo_support_optimizer, E_iterator):
        # Predefines maximum values for change in E and alpha
        maximum_alpha_param = -1
        maximum_delta_E = 0
        E_potential_alpha = 0

        # Define error cache from SMO optimization method
        smo_support_optimizer.error_cache[iterator] = [1, E_iterator]
        valid_error_cache_list = np.nonzero(smo_support_optimizer.error_cache[:, 0].A)[0]

        # Check if error cache list length is significant
        if (len(valid_error_cache_list)) > 1:

            # Iterates through all alpha values in the error cache
            for alpha_param in valid_error_cache_list:

                # Checks if the iterator value matches the alpha value
                if alpha_param == iterator:
                    continue

                # Defines the E holding parameter from the SMO optimizer
                E_param = self.calculate_E_parameter(smo_support_optimizer, alpha_param)
                delta_E = abs(E_iterator - E_param)

                # Checks if change in E holding parameter is differentially larger than the maximum change and if so, redefines the maxes
                if (delta_E > maximum_delta_E):
                    maximum_alpha_param = alpha_param
                    maximum_delta_E = delta_E
                    E_potential_alpha = E_param
            
            return maximum_alpha_param, E_potential_alpha
        else:
            # If the error cache is not significant, defines the alpha value and holding parameter using the helper methods
            potential_alpha = self.select_random_potential_alpha(iterator, smo_support_optimizer.NUM_ROWS)
            E_potential_alpha = self.calculate_E_parameter(smo_support_optimizer, potential_alpha)
        
        """ print("POTENTIAL ALPHA VALUE IS: {}\n\nSMO OPTIMIZATION PARAMETER FOR POTENTIAL ALPHA IS: {}\n".format(potential_alpha, E_potential_alpha)) """
        return potential_alpha, E_potential_alpha

    # ====== METHOD TO SELECT OPTIMIZED ALPHA FROM SMO OPTIMIZER AND PARAMETERS ======
    # ==================== VIA AN OUTER-LOOP ITERATION HEURISTIC =====================
    def outer_loop_heuristic_smo_optimization(self, input_dataset, class_labels, absolute_ceiling_constant, alpha_tolerance, MAX_ITER, kernel_tuple=("lin", 0)):
        # Call the SVM-SMO Support Optimizer object
        smo_support_optimizer = Platt_SMO_Support_Optimization_Structure(np.mat(input_dataset), np.mat(class_labels).transpose(), absolute_ceiling_constant, alpha_tolerance, kernel_tuple, self.TIME_I)

        # Predefine iteration constant and boolean to track full set progress
        iteration_constant = 0
        entire_set_checked = True
        changed_alpha_pairs = 0

        # Iterates while iteration constant falls within method's boundary conditions
        while (iteration_constant < MAX_ITER) and ((changed_alpha_pairs > 0) or (entire_set_checked)):
            changed_alpha_pairs = 0

            # Checks if the entire set has been iterated through already
            if entire_set_checked:
                # Iterates through the input dataset size
                for iterator in range(smo_support_optimizer.NUM_ROWS):
                    # Increments changed alpha pairs from multilevel choice heuristic method
                    changed_alpha_pairs += self.multilevel_choice_heuristic_smo_optimization(iterator, smo_support_optimizer)
                    """ print("FOR THE FULL SET...\n\nITERATION CONSTANT IS: {}\nLOOP ITERATOR IS: {}\nCHANGED ALPHA VALUE PAIRS ARE: \n{}\n".format(iteration_constant, iterator, changed_alpha_pairs)) """
                iteration_constant += 1                     # Increments the iteration constant
            
            else:
                # Creates unbound values from nonzero alpha entries when entire set has not been checked
                unbound_values = np.nonzero((smo_support_optimizer.alphas.A > 0) * (smo_support_optimizer.alphas.A < absolute_ceiling_constant))[0]

                # Iterates through size of unbound values
                for iterator in unbound_values:
                    # Increments changed alpha pairs from multilevel choice heuristic method 
                    changed_alpha_pairs += self.multilevel_choice_heuristic_smo_optimization(iterator, smo_support_optimizer)
                    """ print("FOR THE UNBOUND VALUES...\n\nITERATION CONSTANT IS: {}\nLOOP ITERATOR IS: {}\nCHANGED ALPHA VALUE PAIRS ARE: \n{}\n".format(iteration_constant, iterator, changed_alpha_pairs)) """
                iteration_constant += 1                     # Increments the iteration constant
            
            # Alters checked set boolean based on whether set has been checked (pretty self-explanatory)
            if entire_set_checked:
                entire_set_checked = False
            elif (changed_alpha_pairs == 0):
                entire_set_checked = True
            """ print("FINAL ITERATION NUMBER IS: {}\n".format(iteration_constant)) """
        
        # Get number of support vectors across SVM-SMO
        print("\nSUPPORT VECTORS ALONG THE SAMPLE DATASET FOR THE ADVANCED SVM-SMO ARE:")
        [print(input_dataset[iterator], class_labels[iterator], sep = " --> ") for iterator in range(100) if smo_support_optimizer.alphas[iterator] > 0.0]

        # Prints SVM-SMO beta-values and formatted alphas greater than zero
        print("\nSAVED SVM-SMO BETA VALUE IS: {}\n\nSAVED SVM-SMO ALPHA (GREATER THAN ZERO) VALUES ARE: \n{}\n".format(smo_support_optimizer.beta, smo_support_optimizer.alphas[smo_support_optimizer.alphas > 0]))

        """
        # Performs runtime tracker for particular method
        self.track_runtime()
        """

        return smo_support_optimizer.beta, smo_support_optimizer.alphas

    # ====== METHOD TO SELECT OPTIMIZED ALPHA FROM SMO OPTIMIZER AND PARAMETERS ======
    # ========== VIA A MULTILEVEL SECOND-CHOICE HEURISTIC SELECTION ROUTINE ==========
    def multilevel_choice_heuristic_smo_optimization(self, iterator, smo_support_optimizer):
        E_iterator = self.calculate_E_parameter(smo_support_optimizer, iterator)

        # Checks if iteration constants abide by absolute and relative boundary conditions defined by the ceiling and tolerance levels
        if ((smo_support_optimizer.labels[iterator] * E_iterator < -smo_support_optimizer.alpha_tolerance) and (smo_support_optimizer.alphas[iterator] < smo_support_optimizer.absolute_ceiling_constant)) or ((smo_support_optimizer.labels[iterator] * E_iterator > smo_support_optimizer.alpha_tolerance) and (smo_support_optimizer.alphas[iterator] > 0)):
            potential_alpha, E_potential_alpha = self.inner_loop_heuristic_smo_optimization(iterator, smo_support_optimizer, E_iterator)
            
            # Creates dummy constants to hold old alpha values from method's parent iterator and potential alpha values
            old_alpha_iterator = np.copy(smo_support_optimizer.alphas[iterator])
            old_alpha_potential = np.copy(smo_support_optimizer.alphas[potential_alpha])

            # Checks if iterated labels match the expected potential alpha label values
            if (smo_support_optimizer.labels[iterator] != smo_support_optimizer.labels[potential_alpha]):
                # Defines the alpha's ceiling and floor if there is a mismatch
                alpha_ceiling = min(smo_support_optimizer.absolute_ceiling_constant, smo_support_optimizer.absolute_ceiling_constant + smo_support_optimizer.alphas[potential_alpha] - smo_support_optimizer.alphas[iterator])
                alpha_floor = max(0, smo_support_optimizer.alphas[potential_alpha] - smo_support_optimizer.alphas[iterator])
            else:
                # Defines the alpha's ceiling and floor if there is a match
                alpha_ceiling = min(smo_support_optimizer.absolute_ceiling_constant, smo_support_optimizer.alphas[potential_alpha] + smo_support_optimizer.alphas[iterator])
                alpha_floor = max(0, smo_support_optimizer.alphas[potential_alpha] + smo_support_optimizer.alphas[iterator] - smo_support_optimizer.absolute_ceiling_constant)

            # Checks if floor and ceiling are equivalent and if so, prints for convenience
            if (alpha_ceiling == alpha_floor):
                """ print("\nFOR ALPHA'S BOUNDARY CONSTRAINTS, THE CEILING AND FLOOR ARE FOUND TO BE EQUAL.\n") """
                return 0

            """
            # Defines delta marker value for optimizing alpha value (NOTE: No kernel transformation)
            optimal_alpha_change_marker = 2.0 * smo_support_optimizer.dataset[iterator, :] * smo_support_optimizer.dataset[potential_alpha, :].T - smo_support_optimizer.dataset[iterator, :] * smo_support_optimizer.dataset[iterator, :].T - smo_support_optimizer.dataset[potential_alpha, :] * smo_support_optimizer.dataset[potential_alpha, :].T
            """

            # Defines delta marker value for optimizing alpha value (NOTE: Kernel transformation)
            optimal_alpha_change_marker = 2.0 * smo_support_optimizer.kernel[iterator, potential_alpha] - smo_support_optimizer.kernel[iterator, iterator] - smo_support_optimizer.kernel[potential_alpha, potential_alpha]

            # Checks if optimal alpha marker is zero and if so, prints for convenience
            if optimal_alpha_change_marker >= 0:
                """ print("\nFOR ALPHA'S OPTIMIZATION, THE VALUE OF THE OPTIMAL ALPHA CHANGE MARKER IS EQUAL TO OR GREATER THAN ZERO.\n") """
                return 0

            # Optimizes alpha values based on optimal marker and constraint processing method
            smo_support_optimizer.alphas[potential_alpha] -= smo_support_optimizer.labels[potential_alpha] * (E_iterator - E_potential_alpha) / optimal_alpha_change_marker
            smo_support_optimizer.alphas[potential_alpha] = self.process_alpha_against_constraints(smo_support_optimizer.alphas[potential_alpha], alpha_ceiling, alpha_floor)
            self.update_E_parameter(smo_support_optimizer, potential_alpha)

            # Checks if margin between new and old alphas are too small and if so, prints for convenience
            if (abs(smo_support_optimizer.alphas[potential_alpha] - old_alpha_potential) < 0.00001):
                """ print("\nTHE POTENTIAL ALPHA VALUE IS NOT MOVING ENOUGH.\n") """
                return 0

            # Increments alpha values by SMO optimizer and updates E parameter
            smo_support_optimizer.alphas[iterator] += smo_support_optimizer.labels[potential_alpha] * smo_support_optimizer.labels[iterator] * (old_alpha_potential - smo_support_optimizer.alphas[potential_alpha])
            self.update_E_parameter(smo_support_optimizer, iterator)

            """
            # Produces dummy beta-values to track differential alpha changes (NOTE: no kernel transformation)
            beta1 = smo_support_optimizer.beta - E_iterator - smo_support_optimizer.labels[iterator] * (smo_support_optimizer.alphas[iterator] - old_alpha_iterator) * smo_support_optimizer.dataset[iterator, :] * smo_support_optimizer.dataset[iterator, :].T - smo_support_optimizer.labels[potential_alpha] * (smo_support_optimizer.alphas[potential_alpha] - old_alpha_potential) * smo_support_optimizer.dataset[iterator, :] * smo_support_optimizer.dataset[potential_alpha, :].T
            beta2 = smo_support_optimizer.beta - E_potential_alpha - smo_support_optimizer.labels[iterator] * (smo_support_optimizer.alphas[iterator] - old_alpha_iterator) * smo_support_optimizer.dataset[iterator, :] * smo_support_optimizer.dataset[potential_alpha, :].T - smo_support_optimizer.labels[potential_alpha] * (smo_support_optimizer.alphas[potential_alpha] - old_alpha_potential) * smo_support_optimizer.dataset[potential_alpha, :] * smo_support_optimizer.dataset[potential_alpha, :].T
            """

            # Produces dummy beta-values to track differential alpha changes (NOTE: Kernal transformation)
            beta1 = smo_support_optimizer.beta - E_iterator - smo_support_optimizer.labels[iterator] * (smo_support_optimizer.alphas[iterator] - old_alpha_iterator) * smo_support_optimizer.kernel[iterator, iterator] - smo_support_optimizer.labels[potential_alpha] * (smo_support_optimizer.alphas[potential_alpha] - old_alpha_potential) * smo_support_optimizer.kernel[iterator, potential_alpha]
            beta2 = smo_support_optimizer.beta - E_potential_alpha - smo_support_optimizer.labels[iterator] * (smo_support_optimizer.alphas[iterator] - old_alpha_iterator) * smo_support_optimizer.kernel[iterator, potential_alpha] - smo_support_optimizer.labels[potential_alpha] * (smo_support_optimizer.alphas[potential_alpha] - old_alpha_potential) * smo_support_optimizer.kernel[potential_alpha, potential_alpha]

            # Checks if new alpha values fall within beta-dependent boundary conditions for beta-value reinitialization
            if (0 < smo_support_optimizer.alphas[iterator]) and (smo_support_optimizer.absolute_ceiling_constant > smo_support_optimizer.alphas[iterator]):
                smo_support_optimizer.beta = beta1
            elif (0 < smo_support_optimizer.alphas[potential_alpha]) and (smo_support_optimizer.absolute_ceiling_constant > smo_support_optimizer.alphas[potential_alpha]):
                smo_support_optimizer.beta = beta2
            else:
                smo_support_optimizer.beta = (beta1 + beta2) / 2.0
            return 1
        else:
            return 0

    # ============ METHOD TO REFRESH E PARAMETER FOR SVM SMO OPTIMIZATION ============
    def update_E_parameter(self, smo_support_optimizer, alpha_param):
        # Defines the E holding parameter using the SMO optimizer helper methods
        E_param = self.calculate_E_parameter(smo_support_optimizer, alpha_param)
        smo_support_optimizer.error_cache[alpha_param] = [1, E_param]
        return

    # ======== METHOD TO RETRIEVE HYPERPLANE DISTRIBUTIVE VALUES FROM ALPHAS =========
    def get_hyperplane_from_alphas(self, alphas, input_dataset, class_labels):
        dataset = np.mat(input_dataset)
        labels = np.mat(class_labels).transpose()
        NUM_ROWS, NUM_COLS = np.shape(dataset)          # Grab dataset dimensionalities
        hyperplane = np.zeros((NUM_COLS, 1))            # Predefine hyperplane as array of zeros

        # Iterates through dataset dimensionality to produce hyperplane from alpha value spread
        for iterator in range(NUM_ROWS):
            hyperplane += np.multiply(alphas[iterator] * labels[iterator], dataset[iterator, :].T)

        print("\nHYPERPLANE DISTRIBUTIVE VALUES FROM ALPHA VALUE SPREAD IS: \n{}\n".format(hyperplane))
        return hyperplane

    # ================== METHOD TO CLASSIFY SELECT DATA AGAINST SVM ==================
    def classify_data_with_machine(self, SELECT_INDEX = 0):
        # Produces dataset, label vector, beta and alpha values from explicit methods
        dataset, labels = self.load_dataset()
        beta, alphas = self.outer_loop_heuristic_smo_optimization(dataset, labels, 0.6, 0.001, 40)
        
        # Calculate formatted data matrix and hyperplane distributive values from data and alpha spread
        hyperplane = self.get_hyperplane_from_alphas(alphas, dataset, labels)
        datamat = np.mat(dataset)

        # Calculate SVM data projection from data matrix, hyperplane distributive values, and beta value
        svm_data_projection = datamat * np.mat(hyperplane) + beta
        
        print("PROJECTION OF NEW DATA AT INDEX {} FROM LABEL CLASSIFIER IS: \n{}\n\nEXACT LABEL OF DATA AT INDEX {} IS: \n{}\n".format(SELECT_INDEX, svm_data_projection[SELECT_INDEX], SELECT_INDEX, labels[SELECT_INDEX]))
        
        # Performs runtime tracker for particular method
        return self.track_runtime()

    # ================ METHOD TO BENCHMARK RUNTIME OF SPECIFIC METHOD ================
    # TODO: Refactor so output references name of current method (look up libraries that do this)
    def track_runtime(self):
        # Track ending time of program and determine overall program runtime
        TIME_F = t()
        delta = TIME_F - self.TIME_I

        if delta < 1.5:
            print("\nReal program runtime is {0:.4g} milliseconds.\n".format(delta * 1000))
        else:
            print("\nReal program runtime is {0:.4g} seconds.\n".format(delta))
        return


# ====================================================================================
# ===================== CLASS DEFINITION: SMO SUPPORT OPTIMIZER ======================
# ====================================================================================


class Platt_SMO_Support_Optimization_Structure(object):

    # ======================== CLASS INITIALIZERS/DECLARATIONS =======================
    def __init__(self, input_dataset, class_labels, absolute_ceiling_constant, alpha_tolerance, kernel_tuple, TIME_I):
        self.TIME_I = TIME_I                                                # Initial time for runtime tracker
        self.dataset = input_dataset                                        # Formatted dataset from sample data
        self.labels = class_labels                                          # Class label vector from sample data
        self.absolute_ceiling_constant = absolute_ceiling_constant          # Alpha ceiling constant for SMO boundary parametrization
        self.alpha_tolerance = alpha_tolerance                              # Alpha tolerance for SMO boundary parametrization
        self.NUM_ROWS = np.shape(input_dataset)[0]                          # Constant to hold number of rows of dataset
        self.alphas = np.mat(np.zeros((self.NUM_ROWS, 1)))                  # Alpha value range initialized as array of zeros
        self.beta = 0                                                       # SVM-SMO beta value
        self.error_cache = np.mat(np.zeros((self.NUM_ROWS, 2)))             # Caching value for tracking compounding errors
        self.kernel = np.mat(np.zeros((self.NUM_ROWS, self.NUM_ROWS)))      # Kernel distribution for non/linear data transformations
        for iterator in range(self.NUM_ROWS):
            self.kernel[:, iterator] = Support_Vector_Machine_Algorithm(TIME_I).kernel_transformation_linear_RBF(self.dataset, self.dataset[iterator, :], kernel_tuple)


# ====================================================================================
# ================================ MAIN RUN FUNCTION =================================
# ====================================================================================


# TODO: Refactor method parameters in main() tests as system arguments
def main():
    # Track starting time of program
    TIME_I = t()

    # Initialize class instance of the support vector machine algorithm
    svm = Support_Vector_Machine_Algorithm(TIME_I)

    """
    # Test load_dataset() method on SVM
    dataset, labels = svm.load_dataset()
    """

    """
    # Test basic Platt SMO in SVM with helper methods
    dataset, labels = svm.load_dataset()
    beta, alphas = svm.simple_sequential_minimal_optimization(dataset, labels, 0.6, 0.001, 40)
    """

    """
    # Test advanced Platt SMO in SVM with helper methods, multilevel looping heuristics, and object-oriented storage
    dataset, labels = svm.load_dataset()
    beta, alphas = svm.outer_loop_heuristic_smo_optimization(dataset, labels, 0.6, 0.001, 40)
    hyperplane = svm.get_hyperplane_from_alphas(alphas, dataset, labels)
    """

    """
    # Classify new data using advanced Platt SMO in SVM
    if len(sys.argv) > 1:
        svm.classify_data_with_machine(SELECT_INDEX = int(sys.argv[1]))
    else:
        svm.classify_data_with_machine()
    """

    """
    # Test RBF datasets using kernel transformation with SVM-SMO classifier
    svm.test_kernel_transform_against_rbf()
    """

    # Test handwriting images dataset using kernal transformation with SVM-SMO classifier
    # TODO: Something is wrong with the runtime. Trace and fix? 
    svm.test_handwriting_digits_with_advanced_svm(("lin", 1))

    return print("\nSupport vector machine class algorithm is done.\n")

if __name__ == "__main__":
    main()