"""Service for managing missions and tasks."""

from __future__ import annotations

import logging
from datetime import date

from app.extensions import db
from app.models.mission import Mission, MissionTask
from app.models.subject import Subject

logger = logging.getLogger(__name__)


class MissionService:
    """Service for creating and managing missions and their tasks."""

    @staticmethod
    def create_mission(
        user_id: int,
        subject_id: int,
        mission_date: date,
        title: str,
        tasks: list[dict] | None = None,
    ) -> Mission:
        """Create a new mission with optional tasks.

        Args:
            user_id: The ID of the user creating the mission.
            subject_id: The ID of the subject for this mission.
            mission_date: The date for the mission.
            title: The title of the mission.
            tasks: Optional list of task dicts with 'title', 'description', and 'order'.

        Returns:
            Mission: The created mission.

        Raises:
            ValueError: If the subject doesn't belong to the user.
        """
        # Validate that the subject belongs to the user
        subject = Subject.query.filter_by(id=subject_id, user_id=user_id).first()
        if not subject:
            raise ValueError(f"Subject {subject_id} not found for user {user_id}")

        mission = Mission(
            user_id=user_id,
            subject_id=subject_id,
            mission_date=mission_date,
            title=title,
            status="Pending",
        )

        if tasks:
            for task_data in tasks:
                task = MissionTask(
                    title=task_data.get("title"),
                    description=task_data.get("description"),
                    order=task_data.get("order", 0),
                    completed=False,
                )
                mission.tasks.append(task)

        db.session.add(mission)
        db.session.commit()
        logger.info("Mission %d created for user %s on %s", mission.id, user_id, mission_date)
        return mission

    @staticmethod
    def get_today_mission(user_id: int, mission_date: date | None = None) -> Mission | None:
        """Get the mission for a specific date (defaults to today).

        Args:
            user_id: The ID of the user.
            mission_date: The date to retrieve the mission for (defaults to today).

        Returns:
            Mission | None: The mission for that date, or None if not found.
        """
        if mission_date is None:
            mission_date = date.today()

        mission = Mission.query.filter_by(
            user_id=user_id, mission_date=mission_date
        ).first()
        if mission is not None:
            MissionService.repair_inconsistent_completion(mission)
        return mission

    @staticmethod
    def repair_inconsistent_completion(mission: Mission) -> Mission:
        """Reopen a mission marked Completed while any task is still incomplete.

        Guards against the previous complete path that could set status without
        requiring every mission point to be checked.
        """
        if mission.status != "Completed":
            return mission
        if all(task.completed for task in mission.tasks):
            return mission

        any_done = any(task.completed for task in mission.tasks)
        mission.status = "In Progress" if any_done else "Pending"
        db.session.commit()
        logger.warning(
            "Reopened mission %d: status was Completed with incomplete tasks",
            mission.id,
        )
        return mission

    @staticmethod
    def mark_task_complete(task_id: int, user_id: int, completed: bool = True) -> MissionTask:
        """Mark a mission task as complete or incomplete.

        Also updates the mission status to "In Progress" when any task is
        marked complete, if the mission is still "Pending".

        Args:
            task_id: The ID of the task to mark.
            user_id: The ID of the user (for authorization).
            completed: Whether the task is completed.

        Returns:
            MissionTask: The updated task.

        Raises:
            ValueError: If the task doesn't exist or doesn't belong to the user's mission.
        """
        task = MissionTask.query.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        # Verify the task's mission belongs to the user
        if task.mission.user_id != user_id:
            raise ValueError(f"Task {task_id} does not belong to user {user_id}")

        task.completed = completed

        # Update mission status to "In Progress" if a task is completed
        # and the mission is still "Pending"
        if completed and task.mission.status == "Pending":
            task.mission.status = "In Progress"
            logger.info("Mission %d status changed to In Progress", task.mission.id)

        db.session.commit()
        return task

    @staticmethod
    def get_mission_completion_percentage(mission_id: int) -> float:
        """Get the completion percentage of a mission.

        Args:
            mission_id: The ID of the mission.

        Returns:
            float: Percentage of tasks completed (0-100).

        Raises:
            ValueError: If the mission doesn't exist.
        """
        mission = Mission.query.get(mission_id)
        if not mission:
            raise ValueError(f"Mission {mission_id} not found")

        return mission.get_completion_percentage()

    @staticmethod
    def update_mission_status(mission_id: int, user_id: int, status: str) -> Mission:
        """Update the status of a mission.

        Args:
            mission_id: The ID of the mission.
            user_id: The ID of the user (for authorization).
            status: The new status (Pending, In Progress, or Completed).

        Returns:
            Mission: The updated mission.

        Raises:
            ValueError: If the mission doesn't exist or doesn't belong to the user.
        """
        mission = Mission.query.get(mission_id)
        if not mission:
            raise ValueError(f"Mission {mission_id} not found")

        if mission.user_id != user_id:
            raise ValueError(f"Mission {mission_id} does not belong to user {user_id}")

        if status not in ("Pending", "In Progress", "Completed"):
            raise ValueError(f"Invalid status: {status}")

        mission.status = status
        db.session.commit()
        logger.info("Mission %d status updated to %s", mission_id, status)
        return mission

    @staticmethod
    def complete_mission(mission_id: int, user_id: int) -> Mission:
        """Set the mission status to Completed once every task is done.

        Does not auto-check incomplete tasks — callers must mark mission points
        done first. Idempotent for already-completed missions. Persists
        immediately so the result survives refresh and application restart.

        Args:
            mission_id: The ID of the mission to complete.
            user_id: The ID of the user (for authorization).

        Returns:
            Mission: The completed mission.

        Raises:
            ValueError: If the mission doesn't exist, doesn't belong to the user,
                or still has incomplete tasks.
        """
        mission = Mission.query.get(mission_id)
        if not mission:
            raise ValueError(f"Mission {mission_id} not found")

        if mission.user_id != user_id:
            raise ValueError(f"Mission {mission_id} does not belong to user {user_id}")

        if mission.status == "Completed" and all(t.completed for t in mission.tasks):
            return mission

        incomplete = [t for t in mission.tasks if not t.completed]
        if incomplete:
            if mission.status == "Completed":
                MissionService.repair_inconsistent_completion(mission)
            raise ValueError(
                "Complete all mission points before marking the session complete."
            )

        mission.status = "Completed"
        db.session.commit()
        logger.info("Mission %d marked complete for user %s", mission_id, user_id)
        return mission
