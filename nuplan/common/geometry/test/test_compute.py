import unittest
from unittest.mock import Mock, patch

import numpy as np
import numpy.typing as npt
from shapely.geometry import Polygon

from nuplan.common.actor_state.state_representation import StateSE2
from nuplan.common.geometry.compute import (
    AngularInterpolator,
    compute_distance,
    compute_lateral_displacements,
    principal_value,
    signed_lateral_distance,
    signed_longitudinal_distance,
)


class TestCompute(unittest.TestCase):
    """Tests for compute functions"""

    @patch("nuplan.common.geometry.compute.get_pacifica_parameters")
    def test_signed_lateral_distance(self, mock_pacifica: Mock) -> None:
        """Tests signed lateral distance of ego to polygon"""
        # Setup
        mock_pacifica.return_value = Mock(half_width=1)

        # Function call
        result_0 = signed_lateral_distance(
            StateSE2(1, 1, -np.pi / 2),
            Polygon(
                (
                    (3, 2),
                    (4, 3),
                    (6, 1),
                    (5, 0),
                )
            ),
        )
        result_1 = signed_lateral_distance(
            StateSE2(1, 1, np.pi / 2),
            Polygon(
                (
                    (3, 2),
                    (4, 3),
                    (6, 1),
                    (5, 0),
                )
            ),
        )

        # Assertions
        self.assertAlmostEqual(result_0, 1)
        self.assertAlmostEqual(result_1, -1)

    @patch("nuplan.common.geometry.compute.get_pacifica_parameters")
    def test_signed_longitudinal_distance(self, mock_pacifica: Mock) -> None:
        """Tests signed longitudinal distance of ego to polygon"""
        # Setup
        mock_pacifica.return_value = Mock(half_length=1)

        # Function call
        result_0 = signed_longitudinal_distance(
            StateSE2(1, 1, 0),
            Polygon(
                (
                    (3, 2),
                    (4, 3),
                    (6, 1),
                    (5, 0),
                )
            ),
        )
        result_1 = signed_longitudinal_distance(
            StateSE2(1, 1, np.pi),
            Polygon(
                (
                    (3, 2),
                    (4, 3),
                    (6, 1),
                    (5, 0),
                )
            ),
        )

        # Assertions
        self.assertAlmostEqual(result_0, 1)
        self.assertAlmostEqual(result_1, -1)

    def test_compute_distance(self) -> None:
        """Tests distance between two points"""
        # Setup
        point_0 = StateSE2(8, 8, np.pi)
        point_1 = StateSE2(4, 5, 0)

        # Function call
        result_0 = compute_distance(point_0, point_1)
        result_1 = compute_distance(point_1, point_0)

        # Assertions
        self.assertEqual(result_0, 5)
        self.assertEqual(result_1, 5)

    def test_compute_lateral_displacements(self) -> None:
        """Tests lateral distance between a list of points"""
        # Setup
        state_0 = StateSE2(0, 0, 0)
        state_1 = StateSE2(0, 1, 0)
        state_2 = StateSE2(0, 2, 0)
        state_3 = StateSE2(0, 3, 0)

        # Function call
        result = compute_lateral_displacements([state_0, state_1, state_2, state_3])

        # Assertions
        for i in range(3):
            self.assertEqual(result[i], 1)

    def test_principal_value(self) -> None:
        """Tests principal angle calculation"""
        # Setup
        values: npt.NDArray[np.float64] = np.array([0, np.pi, 2 * np.pi, 3 * np.pi, -4 * np.pi, -3 * np.pi])
        expected_wrapped_0_to_pi: npt.NDArray[np.float64] = np.array([0, np.pi, 0, np.pi, 0, np.pi])
        expected_wrapped_neg_pi_to_pi: npt.NDArray[np.float64] = np.array([0, -np.pi, 0, -np.pi, 0, -np.pi])

        # Function call
        actual_wrapped_0_to_pi = principal_value(values, min_=0)
        actual_wrapped_neg_pi_to_pi = principal_value(values)

        # Assertions
        np.testing.assert_allclose(expected_wrapped_0_to_pi, actual_wrapped_0_to_pi)
        np.testing.assert_allclose(expected_wrapped_neg_pi_to_pi, actual_wrapped_neg_pi_to_pi)


class TestAngularInterpolator(unittest.TestCase):
    """Tests AngularInterpolator class"""

    @patch("nuplan.common.geometry.compute.np.unwrap", Mock)
    @patch("nuplan.common.geometry.compute.interp1d")
    def setUp(self, mock_interp: Mock) -> None:
        """Sets up variables for testing"""
        interpolator = Mock(return_value="interpolated")
        mock_interp.return_value = interpolator
        self.states: npt.NDArray[np.float64] = np.array([1, 2, 3, 4, 5])
        self.angular_states = [[11], [22], [33], [44]]
        self.interpolator = AngularInterpolator(self.states, self.angular_states)

    @patch("nuplan.common.geometry.compute.np.unwrap")
    @patch("nuplan.common.geometry.compute.interp1d")
    def test_initialization(self, mock_interp: Mock, unwrap: Mock) -> None:
        """Tests interpolation for angular states."""
        # Function call
        interpolator = AngularInterpolator(self.states, self.angular_states)
        # Checks
        unwrap.assert_called_with(self.angular_states, axis=0)
        self.assertEqual(mock_interp.return_value, interpolator.interpolator)

    @patch("nuplan.common.geometry.compute.principal_value")
    def test_interpolate(self, principal_value: Mock) -> None:
        """Interpolates single state"""
        state = 1.5
        principal_value.return_value = 1.23

        # Function call
        result = self.interpolator.interpolate(state)

        self.interpolator.interpolator.assert_called_once_with(state)
        principal_value.assert_called_once_with("interpolated")
        self.assertEqual(1.23, result)

    def test_interpolate_real_value(self) -> None:
        """Interpolates multiple state"""
        states: npt.NDArray[np.float64] = np.array([1, 3])
        angular_states = [[3.0, -2.0], [-3.0, 2.0]]
        interpolator = AngularInterpolator(states, angular_states)
        np.testing.assert_allclose(np.array([-np.pi, -np.pi]), interpolator.interpolate(2))


if __name__ == "__main__":
    unittest.main()
