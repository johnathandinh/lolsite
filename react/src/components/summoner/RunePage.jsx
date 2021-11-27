import {Component} from 'react'
import PropTypes from 'prop-types'
import Popover from 'react-tiny-popover'
import numeral from 'numeral'
import {StatModTable} from './StatMod'

import RUNES from '../../constants/runes'

class RunePage extends Component {
  constructor(props) {
    super(props)
    this.state = {
      selected_part: null,
    }

    this.getVersion = this.getVersion.bind(this)
    this.getRune = this.getRune.bind(this)
    this.getPerks = this.getPerks.bind(this)
    this.setDefaultParticipant = this.setDefaultParticipant.bind(this)
    this.partSelection = this.partSelection.bind(this)
  }
  componentDidMount() {
    var version = this.getVersion()
    if (this.props.store.state.runes[version] === undefined) {
      this.props.store.getRunes(version)
    }
    this.setDefaultParticipant()
  }
  componentDidUpdate(_, prevState) {
    if (prevState.selected_part === null) {
      if (this.props.participants !== null) {
        this.setDefaultParticipant()
      }
    }
  }
  setDefaultParticipant() {
    let mypart = this.props.mypart
    let my_id = mypart._id
    let participants = this.props.participants
    if (participants) {
      for (let part of participants) {
        if (part._id === my_id) {
          this.setState({selected_part: part})
          break
        }
      }
    }
  }
  getVersion() {
    var match = this.props.match
    var version = `${match.major}.${match.minor}.1`
    return version
  }
  getRune(rune_id) {
    // get the latest available rune if the queried one doesn't exist
    var version = this.getVersion()
    var rune = this.props.store.getRune(rune_id, version)
    if ([null, undefined].indexOf(rune) >= 0) {
      var max = 0.0
      var max_ver = null
      for (var _version in this.props.store.state.runes) {
        var version_split = _version.split('.')
        var version_num = parseFloat(`${version_split[0]}.${version_split[1]}`)
        if (version_num > max) {
          max = version_num
          max_ver = _version
        }
      }
      if (max_ver !== null) {
        rune = this.props.store.getRune(rune_id, max_ver)
      }
    }
    return rune
  }
  getPerks(part) {
    var perks = []
    if (part === undefined) {
      part = this.state.selected_part
    }
    if (part === null) {
      return []
    }
    var perk
    for (var i = 0; i <= 5; i++) {
      perk = {
        id: part.stats[`perk_${i}`],
        var1: part.stats[`perk_${i}_var_1`],
        var2: part.stats[`perk_${i}_var_2`],
        var3: part.stats[`perk_${i}_var_3`],
      }
      if (perk.id !== 0) {
        perks.push(perk)
      }
    }
    return perks
  }
  partSelection() {
    var match = this.props.match
    // let parts = [...this.props.parent.getTeam100(), ...this.props.parent.getTeam200()]
    let parts = this.props.participants
    return parts.map((part) => {
      var is_selected = false
      var select_style = {
        height: 30,
        width: 30,
        cursor: 'pointer',
      }
      if (this.state.selected_part !== null && part._id === this.state.selected_part._id) {
        is_selected = true
      }
      if (is_selected) {
        select_style = {
          ...select_style,
          borderStyle: 'solid',
          borderWidth: 3,
          borderColor: 'white',
        }
      } else {
        select_style = {
          ...select_style,
          opacity: 0.4,
        }
      }
      return (
        <div key={`${match.id}-${part.id}-rune-champ-image`}>
          {part.champion.image_url === '' && (
            <div
              title={part.summoner_name}
              onClick={() => this.setState({selected_part: part})}
              style={{...select_style}}
            >
              NA
            </div>
          )}
          {part.champion.image.file_30 !== '' && (
            <img
              title={part.summoner_name}
              onClick={() => this.setState({selected_part: part})}
              style={{...select_style}}
              src={part.champion.image.file_30}
              alt=""
            />
          )}
        </div>
      )
    })
  }
  render() {
    let match = this.props.match
    var rune_stat_height = (this.props.match_card_height - 20) / 6
    return (
      <div>
        <div
          style={{
            marginRight: 20,
            display: 'inline-block',
            marginLeft: 35,
            verticalAlign: 'top',
          }}
        >
          {this.partSelection()}
        </div>
        <div style={{display: 'inline-block'}}>
          {this.getPerks().map((perk) => {
            var rune = this.getRune(perk.id)
            var rune_etc = RUNES.data[perk.id]
            if (rune && rune_etc && rune_etc.perkFormat) {
              return (
                <div key={`${match.id}-${perk.id}`} style={{height: rune_stat_height}}>
                  <div style={{display: 'inline-block'}}>
                    <RuneTooltip rune={rune} style={{display: 'inline-block'}}>
                      <img style={{height: 40, paddingRight: 10}} src={rune.image_url} alt="" />
                    </RuneTooltip>

                    <div
                      style={{
                        display: 'inline-block',
                        verticalAlign: 'top',
                      }}
                    >
                      {rune_etc.perkFormat.map((perk_format, j) => {
                        var desc = rune_etc.perkDesc[j]
                        return (
                          <div style={{lineHeight: 1}} key={`${match._id}-${j}`}>
                            <div
                              style={{
                                display: 'inline-block',
                                width: 200,
                              }}
                            >
                              {desc}
                            </div>
                            <div
                              style={{
                                display: 'inline-block',
                                fontWeight: 'bold',
                              }}
                            >
                              {perk_format
                                .replace('{0}', perk[`var${j + 1}`])
                                .replace('{1}', numeral(perk[`var${j + 2}`]).format('00'))
                                .replace('{2}', perk[`var${j + 2}`])}
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                </div>
              )
            } else {
              if (rune) {
                return (
                  <div key={`${match.id}-${perk.id}`}>
                    <div>{rune._id}</div>
                    <div>var1 : {rune.var1}</div>
                    <div>var2 : {rune.var2}</div>
                    <div>var3 : {rune.var3}</div>
                  </div>
                )
              } else {
                return <div key={`${match.id}-${perk.id}`}>{perk.id}</div>
              }
            }
          })}

          {this.getPerks().length === 0 && (
            <div style={{textAlign: 'center', textDecoration: 'underline'}}>No runes set</div>
          )}
        </div>
        {this.state.selected_part && (
          <div style={{display: 'inline-block', margin: 20, verticalAlign: 'top'}}>
            <StatModTable participant={this.state.selected_part} />
          </div>
        )}
      </div>
    )
  }
}
RunePage.propTypes = {
  store: PropTypes.object,
  pageStore: PropTypes.object,
  parent: PropTypes.object,
}

class RuneTooltip extends Component {
  constructor(props) {
    super(props)
    this.state = {
      is_open: false,
    }

    this.toggle = this.toggle.bind(this)
  }
  toggle() {
    this.setState({is_open: !this.state.is_open})
  }
  render() {
    let rune = this.props.rune
    return (
      <Popover
        transitionDuration={0.01}
        isOpen={this.state.is_open}
        position={'top'}
        containerStyle={{'z-index': '11'}}
        content={
          <div>
            <h5 style={{textDecoration: 'underline', marginTop: -5}}>{rune.name}</h5>

            <div dangerouslySetInnerHTML={{__html: rune.long_description}}></div>
          </div>
        }
      >
        <div
          ref={(elt) => {
            this.target_elt = elt
          }}
          style={this.props.style}
          onClick={this.toggle}
          onMouseOver={() => {
            this.setState({is_open: true})
          }}
          onMouseOut={() => this.setState({is_open: false})}
        >
          {this.props.children}
        </div>
      </Popover>
    )
  }
}
RuneTooltip.propTypes = {
  rune: PropTypes.object,
}

export default RunePage
