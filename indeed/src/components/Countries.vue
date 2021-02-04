<template>
  <div>
    <div id="loader"></div>
    <CContainer style="padding: 40px; display: none" id="myDiv" class="animate-bottom">
      <CRow class="d-flex justify-content-between">
        <h3>Banned Countries</h3>
        <CButton color="info">Back</CButton>
      </CRow>
      <div style="margin:4vh"></div>
      <CRow><h6>Banned</h6></CRow>
      <div style="margin:2vh"></div>
      <CRow>
        <CCard style="min-width: 100%">
          <CRow style="margin: 0">
        <span style="display: inline-block " v-for="banCountry in bannedCountries" :key="banCountry.id">
          <span class="chip border border-secondary">
            {{ banCountry.name }}
            <span class="close-btn" @click="onBanCountryClicked(banCountry)">&times;</span>
          </span>
        </span>
          </CRow>
        </CCard>
      </CRow>
      <CRow><h6>Select Banned Countries</h6></CRow>
      <div style="margin:2vh"></div>
      <CRow>
        <CInputCheckbox label="Select all"
                        :custom="true"
                        :checked="selectAll"
                        @change="onSelectAll"/>
      </CRow>
      <div style="margin:2vh"></div>
      <CRow>
        <CCard style="width: 100% !important;">
          <CContainer>
            <CTabs variant="tabs" :active-tab="0">
              <CTab v-for="tab in tabs" :key="tab" :title=tab>
                <div style="margin:4vh"></div>
                <CCol v-for="c in tab.split('')" :key="c">
                  {{ c }}
                  <CContainer style="padding: 20px">
                    <CRow>
                      <CCol md="4" lg="5" v-for="country in filterCountry(c)" :key="country.id">
                        <CInputCheckbox
                            class="country"
                            :label=country.name
                            :custom="true"
                            :checked="country.ban"
                            :style="country.ban ? 'color: #03b1fc': 'black'"
                            @change="onCountryBanStatusChanged(country)"
                        />
                        <div style="margin:2.5vh"></div>
                      </CCol>
                    </CRow>
                  </CContainer>
                </CCol>
              </CTab>
            </CTabs>
          </CContainer>
        </CCard>
      </CRow>
      <CRow class="d-flex justify-content-between">
        <CButton color="outline-dark" @click="onReset">Reset Selection</CButton>
        <CButton color="info" @click="onSaveAll">Save</CButton>
      </CRow>
    </CContainer>
  </div>


</template>

<script>
export default {
  name: 'Countries',
  data() {
    return {
      selectAll: false,
      tabs: ["ABC", "DEF", "GHI", "JKL", "MN", "OPQ", "RST", "UVW", "XYZ"],
      countries: [],
      bannedCountries: [],
    }
  },
  computed: {},
  methods: {
    showPage() {
      document.getElementById("loader").style.display = "none";
      document.getElementById("myDiv").style.display = "block";
    },
    filterCountry(char) {
      const countries = [...this.countries]
      return countries.filter(c => c.letter === char)
    },
    onSelectAll() {
      this.selectAll = !this.selectAll
      console.log("onSelectAll:", this.selectAll)
      for (let i = 0; i < this.countries.length; i++) {
        this.countries[i].ban = this.selectAll
      }
    },
    onCountryBanStatusChanged(country) {
      const banValue = !country.ban

      const url = new URL("http://45.84.224.70/ban/"),
          params = { id: country.id, ban: banValue }
      Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
      fetch(url)
          .then(response => {
            if (response.status === 200) {
              country.ban = banValue
              this.getCountries()
            }
          })
          .catch(error => console.log("ban fn error: ", error))
    },
    onBanCountryClicked(banCountry) {
      this.onCountryBanStatusChanged(banCountry)
    },
    async onReset() {
      this.selectAll = false;
      await this.getCountries()
    },
    onSaveAll() {
      const url = new URL("http://45.84.224.70/banall/"),
          params = { ban: this.selectAll }
      Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
      fetch(url)
          .then(response => {
            if (response.status === 200) {
              this.getCountries()
            }
          })
          .catch(error => console.log("on save all error: ", error))
    },
    getBannedCountries() {
      const countries = [...this.countries]
      this.bannedCountries = countries.filter(c => c.ban)
          // .sort((a, b) => a.letter.localeCompare(b.letter))
    },
    getCountries() {
      fetch('http://45.84.224.70/getcountries/') //
          .then(response => {
            if (response.status === 200)
              return response.json()
            else throw "err"
          })
          .then(data => {
            this.countries = [...data.countries]
            this.getBannedCountries()
            // update select all
            this.selectAll = this.countries.length === this.bannedCountries.length
            this.showPage()
          })
          .catch(error => console.log("getCountries error: ", error));
    },
  },
  async beforeMount() {
    await this.getCountries()
  }

}
</script>

<style scoped lang="css">
.country {
  font-weight: 600;
  font-size: 15px;
}
</style>
