import os
import json
import traceback

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings

from .services import (
    prepare_time_array,
    normalize_frequencies,
    save_tld_matrix,
    run_octave_script
)

class OctaveController:
    OCTAVE_SCRIPT_DIR = getattr(settings, "OCTAVE_SCRIPT_DIR", None)  # configure in settings
    OCTAVE_SCRIPT_NAME = getattr(settings, "OCTAVE_SCRIPT_NAME", None)  # e.g., "Combined_TLD_Function_21_2_2024.m"

    def enter_time(self, request):
        if request.method == "POST":
            from .forms import TripLengthSetupForm
            form = TripLengthSetupForm(request.POST)
            if not form.is_valid():
                return render(request, "trip_length_distribution/index.html", {"form": form})
            minimum = form.cleaned_data["Minimum"]
            maximum = form.cleaned_data["Maximum"]
            intervals = form.cleaned_data["intervals"]

            array_of_time = prepare_time_array(minimum, maximum, intervals)

            # store in session
            request.session["numberOfIntervals"] = intervals
            request.session["minimumTime"] = minimum
            request.session["arrayOfTime"] = array_of_time

            # prepare frequency form
            from .forms import FrequencyForm
            freq_form = FrequencyForm(number_of_intervals=intervals)
            context = {
                "frequency_form": freq_form,
                "minimumTime": minimum,
                "arrayOfTime": array_of_time,
                "numberOfIntervals": intervals,
                "numberOfIntervals_range": range(intervals),
            }
            return render(request, "trip_length_distribution/time.html", context)
        else:
            from .forms import TripLengthSetupForm
            form = TripLengthSetupForm()
            return render(request, "trip_length_distribution/index.html", {"form": form})

    def send_data_to_script(self, request):
        if request.method != "POST":
            return JsonResponse({"status": "error", "message": "Unsupported method"}, status=405)

        try:
            # session validation
            required = ["arrayOfTime", "numberOfIntervals", "minimumTime"]
            if not all(k in request.session for k in required):
                missing = [k for k in required if k not in request.session]
                return JsonResponse({"status": "error", "message": "Session data missing", "missing": missing}, status=400)

            array_of_time = request.session["arrayOfTime"]
            numberOfIntervals = request.session["numberOfIntervals"]

            # collect frequencies
            freqs = []
            for i in range(numberOfIntervals):
                key = f"time{i}"
                try:
                    val = float(request.POST.get(key, 0))
                    if val < 0:
                        return JsonResponse({"status": "error", "message": f"Frequency at interval {i+1} must be non-negative"}, status=400)
                    freqs.append(val)
                except ValueError:
                    return JsonResponse({"status": "error", "message": f"Invalid frequency value for {key}"}, status=400)

            normalized = normalize_frequencies(freqs)
            request.session["frequencies"] = normalized

            # persist to JSON for Octave
            save_tld_matrix(array_of_time, normalized)

            # run Octave script if configured
            if self.OCTAVE_SCRIPT_DIR and self.OCTAVE_SCRIPT_NAME:
                run_octave_script(self.OCTAVE_SCRIPT_DIR, self.OCTAVE_SCRIPT_NAME)
            else:
                # skip if not configured (maybe offline or stub)
                pass

            return redirect("trip_length_distribution:output")
        except Exception as e:
            traceback_str = traceback.format_exc()
            return JsonResponse({
                "status": "error",
                "message": str(e),
                "traceback": traceback_str
            }, status=500)

    def get_fitting_results(self, request):
        numberOfIntervals = request.session.get("numberOfIntervals", 0)
        frequencies = request.session.get("frequencies", [])
        if not frequencies:
            return JsonResponse({"error": "Frequencies not found"}, status=404)

        # assumes the Octave script produces a JSON in MEDIA_ROOT/TLD/fitting_results.json
        fitting_path = os.path.join(settings.MEDIA_ROOT, "TLD", "fitting_results.json")
        if not os.path.exists(fitting_path):
            return JsonResponse({"error": "Fitting results file missing"}, status=404)

        try:
            with open(fitting_path, "r") as f:
                fittingResults = json.load(f)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid fitting results JSON"}, status=500)

        totalFrequencySum = sum(frequencies)
        context = {
            "fittingResults": fittingResults,
            "numberOfIntervals": numberOfIntervals,
            "frequencies": frequencies,
            "totalFrequencySum": totalFrequencySum,
        }
        return render(request, "trip_length_distribution/output.html", context)
