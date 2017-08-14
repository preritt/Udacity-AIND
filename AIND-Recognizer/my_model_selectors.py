import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
#         raise NotImplementedError
        selected_model = None
        min_BIC_likelihood = None

        for components in range(self.min_n_components, self.max_n_components + 1):
            log_likelihood = 0
            try:
                hmm_model = GaussianHMM(n_components=components, covariance_type="diag", n_iter=1000,
                        random_state=self.random_state, verbose=False).fit(self.X,self.lengths)
                logL = hmm_model.score(self.X, self.lengths)
#                 print(logL)
                log_likelihood += logL
                initial_state_probability = components
                variance_means = hmm_model.n_components*components*2
                transition_probabilities = components*(components-1)
                p = initial_state_probability + variance_means + transition_probabilities
                bic_score = -2*(log_likelihood) + p*np.log(len(self.lengths))

                if min_BIC_likelihood == None:
                    best_model = hmm_model
                    best_hidden_states = components
                    min_BIC_likelihood = bic_score
                else:
                    if (bic_score < min_BIC_likelihood):
                        best_model = hmm_model
                        best_hidden_states = components
                        min_BIC_likelihood = bic_score
            except:
                best_hidden_states = self.n_constant
#                     print()

        return self.base_model(best_hidden_states)


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        selected_model = None
        max_DIC_score = None
        for components in range(self.min_n_components, self.max_n_components + 1):
            try:
                hmm_model = GaussianHMM(n_components=components, covariance_type="diag", n_iter=1000,
                        random_state=self.random_state, verbose=False).fit(self.X,self.lengths)
                logL_pxi = hmm_model.score(self.X, self.lengths)
                logL_all_but_pxi = 0
                other_words_total = 0
                for other_word in self.hwords:
                    if other_word != self.this_word:
                        other_x, other_lengths  = self.hwords[other_word]
                        logL_all_but_pxi = logL_all_but_pxi + hmm_model.score(other_x, other_lengths)
                        other_words_total +=1
                dic_score_component = logL_pxi + (1/other_words_total)*logL_all_but_pxi
                if (max_DIC_score == None):
                    max_DIC_score = dic_score_component
                    best_model = hmm_model
                    best_hidden_states = components
                else:
                    if (dic_score_component > max_DIC_score):
                        best_model = hmm_model
                        best_hidden_states = components
                        max_DIC_score = dic_score_component
            except:
                best_hidden_states = self.n_constant
            
                

        return self.base_model(best_hidden_states)



class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection using CV
        # raise NotImplementedError
        split_method = KFold()
        max_log_likelihood = None
        for hidden_states in range(self.min_n_components, self.max_n_components + 1):
            total_log_likelihood = 0
            number_splits = 0
            try: 
                for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                    X_train, lengths_train = combine_sequences(cv_train_idx, self.sequences)
                    X_tests, lengths_tests = combine_sequences(cv_test_idx, self.sequences)

                    hmm_model = GaussianHMM(n_components=hidden_states, covariance_type="diag", n_iter=1000,
                                            random_state=self.random_state, verbose=False).fit(X_train,lengths_train)

                    number_splits+=1
                    logL = hmm_model.score(X_tests, lengths_tests)
                    total_log_likelihood += logL
                    number_splits += 1



                average_log_likelihood = total_log_likelihood/ number_splits
                if max_log_likelihood == None:
                    max_log_likelihood = average_log_likelihood
                    best_hidden_states = hidden_states
                    best_model = hmm_model
                else:
                    if (average_log_likelihood> max_log_likelihood):
                        max_log_likelihood = average_log_likelihood
                        best_hidden_states = hidden_states
                        best_model = hmm_model
            except:
                best_hidden_states = self.n_constant


        return self.base_model(best_hidden_states)
