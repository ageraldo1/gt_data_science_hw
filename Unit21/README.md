# Exoplanet Exploration
___

### **Models Performance**

    + Support Vector Machine (Kernel : rbf)
        + Precision : 81%
        + F1-score : 79%
        + GridSearch Best Parameters:
            + C : 100
            + gamma : 1
            + score : 83%

    + Random Forest
        + Precision : 90%
        + F1-score : 90%

    + K Nearest Neighbors
        + Precision : 81%
        + F1-score : 80%

# Summary
___
Random Forest algorithm presented the best score in comparison against the other two models: Support Vector Machine and K  Nearest Neighbors. Further data analysis is required to figure out the poor performance of SVM and KNN algorithms. How the data is distributed is one of the factors that is causing poor performance for SVM and KNN algorithms. 