import json
from collections import Counter

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .solver import solve

ALLOWED: set[int] = set(range(1, 11)) | {25, 50, 75, 100}
MAX_SMALL_REPEATS = 2  # un petit nombre (1 à 10) ne peut apparaître que deux fois
MAX_LARGE_REPEATS = 1  # un grand nombre (25, 50, 75, 100) ne peut apparaître qu'une fois


@csrf_exempt
@require_POST
def solve_view(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body)
        numbers = [int(n) for n in data["numbers"]]
        target = int(data["target"])
    except (ValueError, KeyError, TypeError):
        return JsonResponse({"error": "Requête invalide."}, status=400)

    if len(numbers) != 6 or any(n not in ALLOWED for n in numbers):
        return JsonResponse(
            {"error": "Il faut 6 nombres : 1 à 10, ou 25, 50, 75, 100."}, status=400)
    counts = Counter(numbers)
    if any(n <= 10 and c > MAX_SMALL_REPEATS for n, c in counts.items()):
        return JsonResponse(
            {"error": "Un petit nombre (1 à 10) ne peut apparaître que deux fois."},
            status=400)
    if any(n > 10 and c > MAX_LARGE_REPEATS for n, c in counts.items()):
        return JsonResponse(
            {"error": "Un grand nombre (25, 50, 75, 100) ne peut apparaître qu'une fois."},
            status=400)
    if not 100 <= target <= 999:
        return JsonResponse(
            {"error": "L'objectif doit être entre 100 et 999."}, status=400)

    return JsonResponse(solve(numbers, target))
