from django.http import JsonResponse
from django.db import connection
from django.db.migrations.executor import MigrationExecutor


def health(request):
    return JsonResponse({"status": "ok"})


def ready(request):
    """Readiness check - verifies DB connection and migrations are applied."""
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        # Check for pending migrations
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        if plan:
            return JsonResponse(
                {"status": "not_ready", "reason": "pending_migrations", "pending_count": len(plan)},
                status=503,
            )

        return JsonResponse({"status": "ready"})

    except Exception as e:
        return JsonResponse(
            {"status": "not_ready", "reason": "database_error", "error": str(e)},
            status=503,
        )