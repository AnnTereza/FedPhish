import flwr as fl
from typing import List, Tuple, Optional
import numpy as np

'''
class SaveModelStrategy(fl.server.strategy.FedAvg):
    def aggregate_fit(
        self,
        rnd: int,
        results: List[Tuple[fl.server.client_proxy.ClientProxy, fl.common.FitRes]],
        failures: List[BaseException],
    ) -> Optional[fl.common.Weights]:
        aggregated_weights = super().aggregate_fit(rnd, results, failures)
        if aggregated_weights is not None:
            # Save aggregated_weights
            print(f"Saving round {rnd} aggregated_weights...")
            np.savez(f"round-{rnd}-weights.npz", *aggregated_weights)
        return aggregated_weights
'''
# Create strategy and run server
strategy = fl.server.strategy.FedAvg(
    min_fit_clients=5,
    min_eval_clients=5,
    min_available_clients = 5,
)

fl.server.start_server(strategy=strategy, config={"num_rounds": 100})
