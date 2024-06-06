import importlib
import time


def measure_time_and_get_result(mod_name, fun_name, param):
    module = importlib.import_module(mod_name)
    function_to_call = getattr(module, fun_name)

    start_time = time.time()
    res = function_to_call(param)
    end_time = time.time()

    time_elapsed = end_time - start_time
    return res, time_elapsed


def compare_results_and_times(res):
    comp = {
        "function_results": {},
        "execution_times": {}
    }

    for module, (res, time_elapsed) in res.items():
        comp["function_results"][module] = res
        comp["execution_times"][module] = time_elapsed

    return comp


if __name__ == "__main__":
    modules_to_test = ["dokladny", "dokladny22", "zachlanny22"]
    function_name = "function_to_test"
    parameter = "data/przyklad_dokladny.xml"

    results = {}

    for module_name in modules_to_test:
        result, elapsed_time = measure_time_and_get_result(module_name, function_name, parameter)
        results[module_name] = (result, elapsed_time)

    comparison = compare_results_and_times(results)

    max_module_length = max(len(module) for module in modules_to_test)

    print("Porównanie wyników:")
    for module, result in comparison["function_results"].items():
        print(f"{module.ljust(max_module_length)}: {result}")

    print("\nPorównanie czasów wykonania:")
    for module, time_taken in comparison["execution_times"].items():
        print(f"{module.ljust(max_module_length)}: {time_taken:.6f} sekund")
