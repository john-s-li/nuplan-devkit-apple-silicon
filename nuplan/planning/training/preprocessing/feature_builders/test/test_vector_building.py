import unittest

from nuplan.common.actor_state.state_representation import Point2D
from nuplan.common.maps.maps_datatypes import SemanticMapLayer
from nuplan.planning.scenario_builder.test.mock_abstract_scenario import MockAbstractScenario
from nuplan.planning.training.preprocessing.feature_builders.vector_builder_utils import (
    LaneOnRouteStatusData,
    LaneSegmentConnections,
    LaneSegmentCoords,
    LaneSegmentGroupings,
    LaneSegmentLaneIDs,
    LaneSegmentRoadBlockIDs,
    LaneSegmentTrafficLightData,
    MapObjectPolylines,
    OnRouteStatusType,
    get_lane_polylines,
    get_map_object_polygons,
    get_neighbor_vector_map,
    get_neighbor_vector_set_map,
    get_on_route_status,
    get_route_lane_polylines_from_roadblock_ids,
    get_route_polygon_from_roadblock_ids,
)


class TestVectorUtils(unittest.TestCase):
    """Test vector building utility functions."""

    def setUp(self) -> None:
        """
        Initializes DB
        """
        scenario = MockAbstractScenario()

        ego_state = scenario.initial_ego_state
        self.ego_coords = Point2D(ego_state.rear_axle.x, ego_state.rear_axle.y)
        self.map_api = scenario.map_api
        self.route_roadblock_ids = scenario.get_route_roadblock_ids()
        self.traffic_light_data = scenario.get_traffic_light_status_at_iteration(0)

        self.radius = 35
        self.map_features = ['LANE', 'LEFT_BOUNDARY', 'RIGHT_BOUNDARY', 'STOP_LINE', 'CROSSWALK', 'ROUTE_LANES']

    def test_get_lane_polylines(self) -> None:
        """
        Test extracting lane/lane connector baseline path and boundary polylines from given map api.
        """
        lanes_mid, lanes_left, lanes_right, lane_ids = get_lane_polylines(self.map_api, self.ego_coords, self.radius)

        assert type(lanes_mid) == MapObjectPolylines
        assert type(lanes_left) == MapObjectPolylines
        assert type(lanes_right) == MapObjectPolylines
        assert type(lane_ids) == LaneSegmentLaneIDs

    def test_get_map_object_polygons(self) -> None:
        """
        Test extracting map object polygons from map.
        """
        for layer in [SemanticMapLayer.CROSSWALK, SemanticMapLayer.STOP_LINE]:
            polygons = get_map_object_polygons(self.map_api, self.ego_coords, self.radius, layer)

            assert type(polygons) == MapObjectPolylines

    def test_get_route_polygon_from_roadblock_ids(self) -> None:
        """
        Test extracting route polygon from map given list of roadblock ids.
        """
        route = get_route_polygon_from_roadblock_ids(self.map_api, self.route_roadblock_ids)

        assert type(route) == MapObjectPolylines

    def test_get_route_lane_polylines_from_roadblock_ids(self) -> None:
        """
        Test extracting route lane polylines from map given list of roadblock ids.
        """
        route = get_route_lane_polylines_from_roadblock_ids(self.map_api, self.ego_coords, self.route_roadblock_ids)

        assert type(route) == MapObjectPolylines

    def test_get_on_route_status(self) -> None:
        """
        Test identifying whether given roadblock lie within goal route.
        """
        route_roadblock_ids = ["0"]
        roadblock_ids = LaneSegmentRoadBlockIDs(["0", "1"])

        on_route_status = get_on_route_status(route_roadblock_ids, roadblock_ids)

        assert type(on_route_status) == LaneOnRouteStatusData
        assert len(on_route_status.on_route_status) == LaneOnRouteStatusData.encoding_dim()
        assert on_route_status.on_route_status[0] == on_route_status.encode(OnRouteStatusType.ON_ROUTE)
        assert on_route_status.on_route_status[1] == on_route_status.encode(OnRouteStatusType.OFF_ROUTE)

    def test_get_neighbor_vector_map(self) -> None:
        """
        Test extracting neighbor vector map information from map api.
        """
        (
            lane_seg_coords,
            lane_seg_conns,
            lane_seg_groupings,
            lane_seg_lane_ids,
            lane_seg_roadblock_ids,
        ) = get_neighbor_vector_map(self.map_api, self.ego_coords, self.radius)

        assert type(lane_seg_coords) == LaneSegmentCoords
        assert type(lane_seg_conns) == LaneSegmentConnections
        assert type(lane_seg_groupings) == LaneSegmentGroupings
        assert type(lane_seg_lane_ids) == LaneSegmentLaneIDs
        assert type(lane_seg_roadblock_ids) == LaneSegmentRoadBlockIDs

    def test_get_neighbor_vector_set_map(self) -> None:
        """
        Test extracting neighbor vector set map information from map api.
        """
        coords, traffic_light_data = get_neighbor_vector_set_map(
            self.map_api,
            self.map_features,
            self.ego_coords,
            self.radius,
            self.route_roadblock_ids,
            self.traffic_light_data,
        )

        # check coords
        for feature_name in self.map_features:
            assert feature_name in coords
            assert type(coords[feature_name]) == MapObjectPolylines

        # check traffic light data
        assert 'LANE' in traffic_light_data
        assert type(traffic_light_data['LANE']) == LaneSegmentTrafficLightData


if __name__ == '__main__':
    unittest.main()
