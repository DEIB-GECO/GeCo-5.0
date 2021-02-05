import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import Home from '../views/Home.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/',
    name: 'GeCo 5.0',
    component: () =>
      import(/* webpackChunkName: "about" */ '../views/gecoAgent.vue')
  },

  {
    path: '/ds',
    name: 'GeCo 5.0',
    component: () =>
      import(
        /* webpackChunkName: "about" */ '../components/toolbox/tools/dataset_list/dataset_list.vue'
      )
  },

  {
    path: '/chart',
    name: 'GeCo 5.0',
    component: () =>
      import(
        /* webpackChunkName: "about" */ '../components/toolbox/tools/data_visualization/charts/Histogram.vue'
      )
  },
  {
    path: '/test',
    name: 'GeCo 5.0',
    component: () =>
      import(/* webpackChunkName: "about" */ '../views/graph_test.vue')
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;
