from elsa import ELSA
from abc import ABC
import torch
from plugins.fastcompare.algo.algorithm_base import (
    AlgorithmBase,
    Parameter,
    ParameterType,
)


class EasyStudyELSA(AlgorithmBase, ABC):
    def __init__(
        self,
        loader,
        positive_threshold,
        latent,
        epochs,
        lr,
        batch_size,
        device,
        verbose,
        **kwargs,
    ):
        self._ratings_df = loader.ratings_df
        self._loader = loader
        self._all_items = self._ratings_df.item.unique()

        self._rating_matrix = (
            self._loader.ratings_df.pivot(index="user", columns="item", values="rating")
            .fillna(0)
            .values
        )

        # Parameters
        self._threshold = positive_threshold
        self._latent = latent
        self._epochs = epochs
        self._lr = lr
        self._batch_size = batch_size
        self._device = device
        self._verbose = verbose

        if self._verbose:
            print("Initializing EasyStudyELSA...")

        self.data = self._prepare_data()
        self.model_wrapper = ELSA(
            n_items=self._rating_matrix.shape[1],
            n_dims=self._latent,
            lr=self._lr,
            device=self._device,
        )

        if self._verbose:
            print("Model created successfully.")

    def _prepare_data(self):
        if self._verbose:
            print("Preparing data...")

        # Prepare data as ELSA expects, this should match what the data loaders from ELSA expect
        tensor_data = torch.tensor(self._rating_matrix, dtype=torch.float32).to(
            self._device
        )
        if self._verbose:
            print("Data preparation complete.")

        return tensor_data

    def fit(self):
        if self._verbose:
            print(f"Training model for {self._epochs} epochs...")

        self.model_wrapper.fit(
            self.data, epochs=self._epochs, batch_size=self._batch_size
        )
        self.item_embeddings_array = (
            torch.nn.functional.normalize(
                self.model_wrapper.get_items_embeddings(), dim=-1
            )
            .cpu()
            .numpy()
        )

        if self._verbose:
            print("Model training complete.")

    def predict(self, selected_items, filter_out_items, k):
        if self._verbose:
            print("Generating predictions...")

        selected_items = torch.tensor(selected_items, dtype=torch.long).to(self._device)
        filter_out_set = set(filter_out_items)

        # Get similar items
        item_ids, scores = self.model_wrapper.similar_items(
            N=k + len(filter_out_items),
            batch_size=128,
            sources=selected_items,
        )

        # Flatten the tensors and convert them to list for easier manipulation
        item_ids = item_ids.view(-1).tolist()
        scores = scores.view(-1).tolist()

        # Filter out items that are in the filter_out_items list
        filtered_items_with_scores = [
            (item, score)
            for item, score in zip(item_ids, scores)
            if item not in filter_out_set
        ]

        # Get the top K unique items
        top_k = [x[0] for x in filtered_items_with_scores[:k]]

        if self._verbose:
            print("Predictions generated successfully.")

        return top_k

    @classmethod
    def name(cls):
        return "JELSA_NOPOST"

    @classmethod
    def parameters(cls):
        return [
            Parameter(
                "latent",
                ParameterType.INT,
                128,
                help="Number of factors of the latent-space",
                help_key="elsa_latent_help",
            ),
            Parameter(
                "positive_threshold",
                ParameterType.FLOAT,
                2.5,  # default threshold for positive feedback
                help="Threshold for conversion of n-ary rating into binary (positive/negative).",
            ),
            Parameter(
                "epochs",
                ParameterType.INT,
                10,
                help="Number of training epochs",
                help_key="elsa_epochs_help",
            ),
            Parameter(
                "lr",
                ParameterType.FLOAT,
                0.1,
                help="Learning rate for the Adam optimizer",
                help_key="elsa_lr_help",
            ),
            Parameter(
                "batch_size",
                ParameterType.INT,
                32,
                help="Batch size for training. The ideal batch size to optimize ELSA is 32 for MovieLens20M, 128 for Netflix prize, and 2048 for the Goodbooks-10k dataset.",
                help_key="elsa_batch_size_help",
            ),
            Parameter(
                "device",
                ParameterType.STRING,
                "cpu",
                help="Device to run the model on ('cuda' or 'cpu').",
                help_key="elsa_device_help",
            ),
            Parameter(
                "verbose",
                ParameterType.BOOL,
                True,
                help="Enable verbose output for debugging",
                help_key="elsa_verbose_help",
            ),
        ]


# Assuming the ELSA classes, functions and utilities are available in the context,
# and you've imported them correctly as in the original ELSA implementation.
