from MPyDATA import ScalarField, VectorField, PeriodicBoundaryCondition
from MPyDATA.arakawa_c.traversals import Traversals
import numpy as np
import pytest

LEFT, RIGHT = 'left', 'right'


class TestPeriodicBoundaryCondition:
    @pytest.mark.parametrize("data", (np.array([1, 2, 3]),))
    @pytest.mark.parametrize("halo", (1, 2, 3))
    @pytest.mark.parametrize("side", (LEFT, RIGHT))
    def test_scalar_1d(self, data, halo, side):
        # arrange
        field = ScalarField(data, halo, (PeriodicBoundaryCondition(),))
        meta_and_data, fill_halos = field.impl
        traversals = Traversals(grid=data.shape, halo=halo, jit_flags={})
        sut, _ = traversals.make_boundary_conditions()

        # act
        sut(*meta_and_data, *fill_halos)

        # assert
        if side == LEFT:
            np.testing.assert_array_equal(field.data[:halo], data[-halo:])
        elif side == RIGHT:
            np.testing.assert_array_equal(field.data[-halo:], data[:halo])
        else:
            raise ValueError()

    @pytest.mark.parametrize("data", (np.array([1, 2, 3]),))
    @pytest.mark.parametrize("halo", [1, 2, 3])
    @pytest.mark.parametrize("side", [LEFT, RIGHT])
    def test_vector_1d(self, data, halo, side):
        # arrange
        field = VectorField((data,), halo, (PeriodicBoundaryCondition(),))
        meta_and_data, fill_halos = field.impl
        traversals = Traversals(grid=data.shape, halo=halo, jit_flags={})
        _, sut = traversals.make_boundary_conditions()

        # act
        sut(*meta_and_data, *fill_halos)

        # assert
        # TODO!
        print(field.data)
