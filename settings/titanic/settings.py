FEATURES = ['Pclass', 'Sex', 'Age', 'FamilySize', 'Title']
NORMALIZED_TITLES = {"Capt": "Officer",
                     "Col": "Officer",
                     "Major": "Officer",
                     "Jonkheer": "Royalty",
                     "Don": "Royalty",
                     "Sir": "Royalty",
                     "Dr": "Officer",
                     "Rev": "Officer",
                     "the Countess": "Royalty",
                     "Dona": "Royalty",
                     "Mme": "Mrs",
                     "Mlle": "Miss",
                     "Ms": "Mrs",
                     "Mr": "Mr",
                     "Mrs": "Mrs",
                     "Miss": "Miss",
                     "Master": "Master",
                     "Lady": "Royalty"}