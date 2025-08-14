"""
Testes automatizados para o exercício de otimização de modelos
"""

import numpy as np
import pandas as pd
import pytest
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


class TestModelOptimization:
    """Testes para validação e otimização de modelos"""

    @classmethod
    def setup_class(cls):
        """Setup dos dados de teste"""
        wine = load_wine()
        cls.X, cls.y = wine.data, wine.target
        cls.X_train, cls.X_test, cls.y_train, cls.y_test = train_test_split(
            cls.X, cls.y, test_size=0.3, random_state=42, stratify=cls.y
        )

    def test_data_preparation(self):
        """Testa se os dados foram preparados corretamente"""
        # Verificar se os dados foram carregados
        assert hasattr(self, "X") and hasattr(self, "y")
        assert self.X.shape[0] == self.y.shape[0]

        # Verificar divisão treino/teste
        assert hasattr(self, "X_train") and hasattr(self, "X_test")
        assert hasattr(self, "y_train") and hasattr(self, "y_test")

        # Verificar proporções aproximadas (70-30)
        total_samples = len(self.X)
        train_ratio = len(self.X_train) / total_samples
        assert 0.65 <= train_ratio <= 0.75, f"Ratio treino deve ser ~0.7, got {train_ratio}"

    def test_stratified_cv_manual(self):
        """Testa implementação manual de stratified CV"""

        def stratified_cv_manual(X, y, model, k=5):
            """Implementação de referência para comparação"""
            from sklearn.model_selection import StratifiedKFold

            skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
            scores = []

            for train_idx, val_idx in skf.split(X, y):
                X_train_fold, X_val_fold = X[train_idx], X[val_idx]
                y_train_fold, y_val_fold = y[train_idx], y[val_idx]

                model_copy = LogisticRegression(random_state=42, max_iter=1000)
                model_copy.fit(X_train_fold, y_train_fold)
                score = model_copy.score(X_val_fold, y_val_fold)
                scores.append(score)

            return scores

        # Testar implementação
        model = LogisticRegression(random_state=42, max_iter=1000)
        scores = stratified_cv_manual(self.X_train, self.y_train, model, k=5)

        # Verificar se retorna 5 scores
        assert len(scores) == 5, f"Esperado 5 scores, got {len(scores)}"

        # Verificar se scores são razoáveis (entre 0 e 1)
        assert all(0 <= score <= 1 for score in scores), "Scores devem estar entre 0 e 1"

        # Verificar se média está em range razoável para este dataset
        mean_score = np.mean(scores)
        assert mean_score > 0.8, f"Score muito baixo: {mean_score}"

    def test_model_comparison(self):
        """Testa comparação entre diferentes modelos"""
        models = {
            "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
            "Random Forest": RandomForestClassifier(random_state=42),
            "SVM": SVC(random_state=42),
        }

        cv_results = {}
        for name, model in models.items():
            scores = cross_val_score(model, self.X_train, self.y_train, cv=5, scoring="accuracy")
            cv_results[name] = scores

        # Verificar se todos os modelos foram testados
        assert len(cv_results) == 3, "Devem haver resultados para 3 modelos"

        # Verificar se scores são razoáveis
        for name, scores in cv_results.items():
            assert len(scores) == 5, f"Modelo {name} deve ter 5 scores"
            assert np.mean(scores) > 0.7, f"Modelo {name} com performance muito baixa"

    def test_random_forest_grid_search(self):
        """Testa otimização do Random Forest com Grid Search"""
        rf_param_grid = {"n_estimators": [50, 100], "max_depth": [3, 5, None], "min_samples_split": [2, 5]}

        rf_grid = GridSearchCV(
            RandomForestClassifier(random_state=42),
            rf_param_grid,
            cv=3,  # Usar 3 folds para acelerar teste
            scoring="accuracy",
        )

        rf_grid.fit(self.X_train, self.y_train)

        # Verificar se encontrou melhores parâmetros
        assert hasattr(rf_grid, "best_params_"), "Grid search deve ter best_params_"
        assert hasattr(rf_grid, "best_score_"), "Grid search deve ter best_score_"

        # Verificar se score melhorou vs baseline
        baseline_rf = RandomForestClassifier(random_state=42)
        baseline_scores = cross_val_score(baseline_rf, self.X_train, self.y_train, cv=3)
        baseline_mean = np.mean(baseline_scores)

        # Grid search deve ser pelo menos tão bom quanto baseline
        assert rf_grid.best_score_ >= baseline_mean - 0.05, "Grid search não deve piorar muito vs baseline"

    def test_svm_random_search(self):
        """Testa otimização do SVM com Random Search"""
        from scipy.stats import uniform
        from sklearn.model_selection import RandomizedSearchCV

        svm_param_dist = {"C": uniform(0.1, 10), "gamma": ["scale", "auto"], "kernel": ["rbf", "linear"]}

        svm_random = RandomizedSearchCV(
            SVC(random_state=42),
            svm_param_dist,
            n_iter=10,  # Poucos iter para acelerar teste
            cv=3,
            scoring="accuracy",
            random_state=42,
        )

        svm_random.fit(self.X_train, self.y_train)

        # Verificar se funcionou
        assert hasattr(svm_random, "best_params_"), "Random search deve ter best_params_"
        assert hasattr(svm_random, "best_score_"), "Random search deve ter best_score_"
        assert svm_random.best_score_ > 0.7, "SVM otimizado deve ter score razoável"

    def test_pipeline_with_preprocessing(self):
        """Testa pipeline com pré-processamento"""
        pipe = Pipeline([("scaler", StandardScaler()), ("classifier", SVC(random_state=42))])

        pipe_param_grid = {"classifier__C": [0.1, 1, 10], "classifier__gamma": ["scale", "auto"]}

        pipe_grid = GridSearchCV(pipe, pipe_param_grid, cv=3, scoring="accuracy")

        pipe_grid.fit(self.X_train, self.y_train)

        # Verificar se pipeline funcionou
        assert hasattr(pipe_grid, "best_estimator_"), "Pipeline deve ter best_estimator_"

        # Verificar se pode fazer predições
        y_pred = pipe_grid.predict(self.X_test)
        assert len(y_pred) == len(self.y_test), "Predições devem ter mesmo tamanho que teste"

        # Verificar accuracy razoável
        accuracy = accuracy_score(self.y_test, y_pred)
        assert accuracy > 0.8, f"Pipeline deve ter accuracy > 0.8, got {accuracy}"

    def test_final_model_evaluation(self):
        """Testa avaliação final dos modelos"""
        # Modelos para testar
        models = {
            "RF": RandomForestClassifier(random_state=42),
            "SVM": SVC(random_state=42),
            "LR": LogisticRegression(random_state=42, max_iter=1000),
        }

        test_scores = {}
        for name, model in models.items():
            model.fit(self.X_train, self.y_train)
            score = model.score(self.X_test, self.y_test)
            test_scores[name] = score

        # Verificar se todos os modelos foram avaliados
        assert len(test_scores) == 3, "Devem haver scores para 3 modelos"

        # Verificar se pelo menos um modelo tem performance boa
        best_score = max(test_scores.values())
        assert best_score > 0.85, f"Melhor modelo deve ter score > 0.85, got {best_score}"

    def test_hyperparameter_improvement(self):
        """Testa se otimização de hiperparâmetros melhora performance"""
        # Baseline Random Forest
        rf_baseline = RandomForestClassifier(random_state=42)
        baseline_scores = cross_val_score(rf_baseline, self.X_train, self.y_train, cv=3)
        baseline_mean = np.mean(baseline_scores)

        # Random Forest otimizado
        rf_param_grid = {"n_estimators": [50, 100, 200], "max_depth": [3, 5, None]}

        rf_grid = GridSearchCV(RandomForestClassifier(random_state=42), rf_param_grid, cv=3, scoring="accuracy")

        rf_grid.fit(self.X_train, self.y_train)

        # Otimização deve manter ou melhorar performance
        improvement = rf_grid.best_score_ - baseline_mean
        assert improvement >= -0.02, f"Otimização não deve piorar muito: {improvement}"

    def test_cross_validation_consistency(self):
        """Testa consistência dos resultados de CV"""
        model = LogisticRegression(random_state=42, max_iter=1000)

        # Executar CV múltiplas vezes com mesmo random_state
        scores1 = cross_val_score(model, self.X_train, self.y_train, cv=5, random_state=42)
        scores2 = cross_val_score(model, self.X_train, self.y_train, cv=5, random_state=42)

        # Resultados devem ser idênticos com mesmo random_state
        np.testing.assert_array_almost_equal(scores1, scores2, decimal=6)

        # Variabilidade entre folds deve ser razoável
        std_score = np.std(scores1)
        assert std_score < 0.1, f"Variabilidade entre folds muito alta: {std_score}"


def test_data_leakage_prevention():
    """Testa se não há vazamento de dados"""
    wine = load_wine()
    X, y = wine.data, wine.target

    # Simular preprocessamento incorreto (vazamento)
    scaler_wrong = StandardScaler()
    X_scaled_wrong = scaler_wrong.fit_transform(X)  # Fit em todo dataset - ERRADO

    X_train, X_test, y_train, y_test = train_test_split(X_scaled_wrong, y, test_size=0.3, random_state=42)

    # Preprocessamento correto
    X_train_orig, X_test_orig, y_train_orig, y_test_orig = train_test_split(X, y, test_size=0.3, random_state=42)

    scaler_correct = StandardScaler()
    X_train_scaled = scaler_correct.fit_transform(X_train_orig)
    X_test_scaled = scaler_correct.transform(X_test_orig)

    # Treinar modelo em ambos os casos
    model1 = LogisticRegression(random_state=42, max_iter=1000)
    model2 = LogisticRegression(random_state=42, max_iter=1000)

    model1.fit(X_train, y_train)  # Com vazamento
    model2.fit(X_train_scaled, y_train_orig)  # Sem vazamento

    score1 = model1.score(X_test, y_test)
    score2 = model2.score(X_test_scaled, y_test_orig)

    # Score com vazamento pode ser artificialmente alto
    # Diferença não deve ser muito grande se implementado corretamente
    assert abs(score1 - score2) < 0.15, "Possível vazamento de dados detectado"


if __name__ == "__main__":
    # Executar testes
    pytest.main([__file__])
