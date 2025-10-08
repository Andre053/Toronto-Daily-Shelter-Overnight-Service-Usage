import { FeatureCollection } from "geojson";

export type DataPoint = {
    value: number;
    date: Date;
}

export type StatByFsa = {
  [key: string]: number;
}

export type MonthlyStatsFsa = {
  YEAR: number;
  MONTH: number;
  FSA: string;
  STATS: Stats;
}

export type MonthlyStats = {
  YEAR: number;
  MONTH: string;
  STATS: Stats;
}

export type YearlyStats = {
  YEAR: number;
  STATS: Stats;
}

export type AllStatsDaily = {
  STATS: Stats;
}

export type AllStatsFsa = {
  FSA: string;
  STATS: Stats;
}

export type Stats = {
  MEAN_SERVICE_USERS: number;
  MAX_SERVICE_USERS: number;
  MIN_SERVICE_USERS: number;
  MEAN_CAPACITY_ACTUAL_BED: number;
  MAX_CAPACITY_ACTUAL_BED: number;
  MIN_CAPACITY_ACTUAL_BED: number;
  MEAN_CAPACITY_FUNDING_BED: number;
  MAX_CAPACITY_FUNDING_BED: number;
  MIN_CAPACITY_FUNDING_BED: number;
  MEAN_OCCUPIED_BEDS: number;
  MAX_OCCUPIED_BEDS: number;
  MIN_OCCUPIED_BEDS: number;
  MEAN_UNOCCUPIED_BEDS: number;
  MAX_UNOCCUPIED_BEDS: number;
  MIN_UNOCCUPIED_BEDS: number;
  MEAN_OCCUPIED_ROOMS: number;
  MAX_OCCUPIED_ROOMS: number;
  MIN_OCCUPIED_ROOMS: number;
  MEAN_UNOCCUPIED_ROOMS: number;
  MAX_UNOCCUPIED_ROOMS: number;
  MIN_UNOCCUPIED_ROOMS: number;
  UNIQUE_ORG_COUNT: number;
  UNIQUE_PROGRAM_COUNT: number;
  UNIQUE_SHELTER_COUNT: number;
  UNIQUE_LOCATION_COUNT: number;
}

export type StatsKey = keyof Stats;

export type DataByMonth = {
  month: string;
  data: DataCategory[];
}
export type DataCategory = {
  LOCATION_FSA_CODE: string;
  SERVICE_USER_COUNT_MEAN: number;
  CAPACITY_ACTUAL_BED: number;
  CAPACITY_FUNDING_BED: number;
  OCCUPIED_BEDS_MEAN: number;
  UNOCCUPIED_BEDS_MEAN: number;
  OCCUPIED_ROOMS_MEAN: number;
  UNOCCUPIED_ROOMS_MEAN: number;
  PROGRAM_COUNT: number;
  SHELTER_COUNT: number;
  LOCATION_COUNT: number;
  ORG_COUNT: number;
}


export type ChartOpts = {
  [key: string]: ChartOption[];
}

export type ChartOption = {
  displayName: string;
  dataKey: string;
  selectedStatus: boolean;
}

export type DataByFeaturePayload = {
  statName: string;
  startDate: string;
  endDate: string;
  dataByFeature: DataByFeature;
}

export type DataByFeature = {
  [key: string]: number[];
}

export type AreaData = {
  [key: string]: string | string[] | any
}

export type GeoData = {
  name: string,
  featureCollection: FeatureCollection
}

export type ServerData = {
  message: string;
  data: any;
}

export type ServiceUserDataAll = {
  [key: string]: ServiceUserDataByFsa[];
}

type ServiceUserDataByFsa = {
  total_sum: number;
  total_mean: number;
  daily_stats: ServiceUserDailyStats[];
}
type ServiceUserDailyStats = {
  date: string;
  service_user_sum: number;
  service_user_mean: number
}

export type FsaData = {
    fsa: fsaCounts[];
    stats: FsaStats;
}

export type fsaCounts = {
  key: string;
  val: number;
}
export type FsaStats = {
  max: number;
}

export type OccupancyData = {
  occupancyDate: string;
  organizationName: string;
  shelterId: number;
  shelterGroup: string;
  locationName: string;
  locationAddress: string;
  locationPostalCode: string;
  locationCity: string;
  programId: number;
  programName: string;
  programModel: string;
  programSector: string;
  overnightServiceType: string;
}
